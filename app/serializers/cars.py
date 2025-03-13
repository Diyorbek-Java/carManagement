from rest_framework import serializers

from ..models.cars import Car,CarImages

class CarImageSeriazlier(serializers.ModelSerializer):

    class Meta:
        model = CarImages
        fields = "__all__"
    
class CarImagesGetSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = CarImages
        fields = "__all__"
    def get_photo(self, obj):
        return obj.photo.url


class CarGetSerializer(serializers.ModelSerializer):
    images = CarImagesGetSerializer(many=True, required=False)
    class Meta:
        model = Car
        fields = '__all__'
        extra_fields = ["images"]

class CarSerializer(serializers.ModelSerializer):
    images = serializers.FileField(required=False)
    class Meta:
        model = Car
        fields = '__all__'
        extra_fields = ["images"]
