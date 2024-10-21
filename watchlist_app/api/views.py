from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from watchlist_app.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination
from watchlist_app.api.permissions import AdminOrReadonly, ReviewerOrReadOnly
from watchlist_app.models import WatchList, StreamingPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamingPlatformSerializer, ReviewSerializer
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThottle




class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(reviewer__username=username)
    
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(reviewer__username=username)



class WatchListAV(APIView):
    permission_classes = [AdminOrReadonly]
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class WatchListDetailAV(APIView):
    permission_classes = [AdminOrReadonly]
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'Error': 'The movie doesnot exists'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie, context={'request': request})
        return Response(serializer.data)
    
    
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    
class StreamingPlatformVS(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadonly]
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = StreamingPlatform.objects.all().order_by('name')
    serializer_class = StreamingPlatformSerializer
    
    
    
    
# class StreamingPlatformVS(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#     def list(self, request):
#         queryset = StreamingPlatform.objects.all()
#         serializer = StreamingPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamingPlatform.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = StreamingPlatformSerializer(user)
#         return Response(serializer.data)
    
    
#     def create(self, request):
#         serializer = StreamingPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StreamingPlatformAV(APIView):
    
    def get(self, request):
        names = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializer(names, many=True, context={'request': request})
        return Response(serializer.data)
    
    
    def post(self, request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
class StreamingPlatformDetailsAV(APIView):
    
    def get(self, request, pk):
        try:
            name = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            return Response({'Error': 'Streaming Platform doesnot exists'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamingPlatformSerializer(name, context={'request': request})
        return Response(serializer.data)
    
    
    def put(self, request, pk):
        name = StreamingPlatform.objects.get(pk=pk)
        serializer = StreamingPlatformSerializer(name, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request, pk):
        name = StreamingPlatform.objects.get(pk=pk)
        name.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    
    
class ReviewCreateAV(generics.CreateAPIView):
    throttle_classes = [ReviewCreateThrottle]
    serializer_class = ReviewSerializer
    
    
    def get_queryset(self):
        return Review.objects.all()
    
    
    def perform_create(self, serializer):
        permission_classes = [IsAuthenticated]
        pk = self.kwargs['pk']
        movie = WatchList.objects.get(pk=pk)
        
        reviewer = self.request.user
        
        queryset = Review.objects.filter(movie=movie, reviewer=reviewer)
        
        new_rating = serializer.validated_data['rating']
        
        if movie.avg_rating == 0:
            movie.number_of_ratings == 0
        
        if movie.number_of_ratings == 0:
            movie.avg_rating = new_rating
        else:
            movie.avg_rating = (movie.avg_rating*movie.number_of_ratings+new_rating)/(movie.number_of_ratings+1)
        movie.number_of_ratings +=1
        movie.save()
        
        if queryset.exists():
            raise ValidationError("You have already submitted your review")
        
        serializer.save(movie=movie, reviewer=reviewer)
    
    
class ReviewAV(generics.ListAPIView):
    # throttle_classes = [ReviewListThottle]
    # permission_classes = [IsAuthenticated]
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reviewer__username', 'rating']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(movie=pk)
    
    
class ReviewDetailsAV(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ReviewerOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    
    
    
class WatchListGV(generics.ListAPIView):
    pagination_class = WatchListCPagination
    serializer_class=WatchListSerializer
    queryset = WatchList.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title', 'platform__name']
    
    
    
# class ReviewAV(APIView):
    
#     def get(self, request):
#         reviews = Review.objects.all()
#         serializer = ReviewSerializer(reviews, many=True, context={'request': request})
#         return Response(serializer.data)
    
    
#     def post(self, request):
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class ReviewAV(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
        
        

# class ReviewDetailsAV(APIView):
    
#     def get(self, request, pk):
#         try:
#             review = Review.objects.get(pk=pk)
#         except Review.DoesNotExist:
#             return Response({'Error': 'Review with that Id doesnot exists'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ReviewSerializer(review, context={'request': request})
#         return Response(serializer.data)
    
    
    
#     def put(self, request, pk):
#         review = Review.objects.get(pk=pk)
#         serializer = ReviewSerializer(review, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
#     def delete(self, request, pk):
#         review = Review.objects.get(pk=pk)
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)





  



        

























# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method=='GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializers(movies, many=True)
#         return Response(serializer.data)
#     if request.method=='POST':
#         serializer = MovieSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.error)


# @api_view(['GET', 'PUT', 'DELETE'])
# def movieById(request, mId):
#     if request.method=='GET':
#         try:
#             movies = Movie.objects.get(pk=mId)
#         except Movie.DoesNotExist:
#             return Response({'Error':'Movie doesnot exist'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializers(movies)
#         return Response(serializer.data)
    
#     if request.method=='PUT':
#         movie = Movie.objects.get(pk=mId)
#         serializer = MovieSerializers(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method=='DELETE':
#         movie = Movie.objects.get(pk=mId)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)