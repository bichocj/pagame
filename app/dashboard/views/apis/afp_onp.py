from rest_framework import viewsets

from core.models import AfpOnp
from .utils import BasePathSerializer


class AfpOnpPathSerializer(BasePathSerializer):
    @staticmethod
    def get_path():
        return "afp-onp"

    class Meta:
        model = AfpOnp
        fields = ["name", "mandatory", "prima", "commision", "url"]


class AfpOnpViewSet(viewsets.ModelViewSet):
    queryset = AfpOnp.objects.all()
    serializer_class = AfpOnpPathSerializer
