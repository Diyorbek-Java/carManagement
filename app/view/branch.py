from rest_framework import viewsets

from ..serializers.branch import BrachNameSerializer,BranchAllSerializer
from ..models.branch import Branch
from ..pagination .paginations import DefaultLimitOffSetPagination
from rest_framework.permissions import IsAuthenticated

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchAllSerializer
    pagination_class = DefaultLimitOffSetPagination
    # permission_classes = [IsAuthenticated]