
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