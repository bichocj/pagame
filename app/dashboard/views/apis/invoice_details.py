from rest_framework import viewsets

from core.models import InvoiceDetails
from .utils import BasePathSerializer


class InvoiceDetailsPathSerializer(BasePathSerializer):
    @staticmethod
    def get_path():
        return "invoice-details"

    class Meta:
        model = InvoiceDetails
        fields = ["invoice", "concept", "amount", "concept_type", "url"]


class InvoiceDetailsViewSet(viewsets.ModelViewSet):
    queryset = InvoiceDetails.objects.all()
    serializer_class = InvoiceDetailsPathSerializer
