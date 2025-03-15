
import re, json
from rest_framework import serializers
from ..models.branch import Branch

class BranchAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

class BrachNameSerializer(serializers.ModelSerializer):
    class Meta:
        model= Branch
        fields =("id","name")


class BranchCreateSerializer(serializers.ModelSerializer):
    google_map_link = serializers.CharField(write_only=True)

    class Meta:
        model = Branch
        fields = ['name', 'address', 'status', 'year_of_construction', 'total_area', 'google_map_link']

    def extract_lat_long_from_url(self, url):
        # Extract latitude and longitude from the Google Maps URL
        # This is a simplified example, you may need to adjust the regex based on the actual URL format
        match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
        if match:
            return match.group(1), match.group(2)
        return "", ""

    def create(self, validated_data):
        google_map_link = validated_data.pop('google_map_link')
        latitude, longitude = self.extract_lat_long_from_url(google_map_link)

        if latitude and longitude:
            validated_data['latitude'] = latitude
            validated_data['longitude'] = longitude

        branch = Branch.objects.create(**validated_data)
        return branch