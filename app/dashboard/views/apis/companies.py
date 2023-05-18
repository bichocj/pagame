from rest_framework import viewsets

from core.models import Company
from .utils import BasePathSerializer


class CompanyPathSerializer(BasePathSerializer):
    @staticmethod
    def get_path():
        return "company"

    class Meta:
        model = Company
        fields = ["name", "ruc", "address", "signer_name", "signer_title", "url"]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyPathSerializer
