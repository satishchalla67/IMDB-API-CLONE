
from rest_framework import serializers
from watchlist_app.models import WatchList, StreamingPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    
    reviewer = serializers.StringRelatedField()
    
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ('movie',)


class WatchListSerializer(serializers.ModelSerializer):
    
    #reviews = ReviewSerializer(many=True, read_only=True)
    
    platform = serializers.StringRelatedField()
    
    len_name = serializers.SerializerMethodField()
    
    class Meta:
        model = WatchList
        fields = "__all__"
        # fields = ['title', 'storyline','reviews', 'platform', 'len_name']
        # exclude = ['active']
        
        
    def get_len_name(self, object):
        return len(object.title)


class StreamingPlatformSerializer(serializers.ModelSerializer):
    
    watchlist = WatchListSerializer(many=True, read_only=True)
    
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='watchlistdetail',
    # )
    
    len_name = serializers.SerializerMethodField()
    
    class Meta:
        model = StreamingPlatform
        fields = "__all__"
        
        
    def get_len_name(self, object):
        return len(object.name)
        



        
        
    # def validate_name(self, value):
    #     if len(value)<2:
    #         raise serializers.ValidationError("Title of the movie cannot be 1 letter")
    #     return value
    
    # def validate(self, data):
    #     if data['name']==data['description']:
    #         raise serializers.ValidationError("Title and description cannot be same")
    #     return data


# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError("Title of the movie cannot be 1 letter")

# class MovieSerializers(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
    
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
    
#     def validate_name(self, value):
#         if len(value)<2:
#             raise serializers.ValidationError("Title of the movie cannot be 1 letter")
#         return value
    
#     def validate(self, data):
#         if data['name']==data['description']:
#             raise serializers.ValidationError("Title and description cannot be same")
#         return data