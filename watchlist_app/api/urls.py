from django.urls import include, path
# from .views import movie_list, movieById
from .views import WatchListAV, WatchListDetailAV, StreamingPlatformAV, StreamingPlatformDetailsAV, ReviewAV, ReviewDetailsAV, ReviewCreateAV, StreamingPlatformVS, UserReview, WatchListGV
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('streamingplatform', StreamingPlatformVS, basename='streaming-platform')

urlpatterns = [
    path('watchlist/', WatchListAV.as_view(), name='watchlist'),
    path('watchlist/<int:pk>/', WatchListDetailAV.as_view(), name='watchlist-detail'),
    # path('streamingplatform/', StreamingPlatformAV.as_view(), name='streamingplatform'),
    # path('streamingplatform/<int:pk>/', StreamingPlatformDetailsAV.as_view(), name='streamingplatform-detail'),
    path('', include(router.urls)),
    
    
    path('<int:pk>/review-create/', ReviewCreateAV.as_view(), name='review-create'),
    path('<int:pk>/review/', ReviewAV.as_view(), name='review'),
    path('review/<int:pk>/', ReviewDetailsAV.as_view(), name='review-detail'),
    path('reviews/', UserReview.as_view(), name='user-review'),
    path('watchlist2/', WatchListGV.as_view(), name='watch-list'),
    
]

# SIMPLE_JWT = {
#     "ROTATE_REFRESH_TOKENS" : True 
# }