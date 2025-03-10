from rest_framework import viewsets

from ..serializers.branch import BrachNameSerializer,BranchAllSerializer
from ..models.branch import Branch

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchAllSerializer