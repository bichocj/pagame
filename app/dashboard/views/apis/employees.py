from rest_framework import viewsets, serializers

from core.models import Employ
from .utils import BasePathSerializer


class EmployPathSerializer(BasePathSerializer):
    persona = serializers.StringRelatedField(source="person")
    afp__onp = serializers.StringRelatedField(source="afp_onp")

    @staticmethod
    def get_path():
        return "employees"

    class Meta:
        model = Employ
        fields = [
            "persona",
            "person",
            "salary",
            "afp__onp",
            "afp_onp",
            "has_children",
            "bank_name",
            "bank_account_number",
            "bank_account_number_cci",
            "url",
        ]
        extra_kwargs = {
            "employ": {"write_only": True},
            "afp_onp": {"write_only": True},
            "person": {"write_only": True},
        }


class EmployViewSet(viewsets.ModelViewSet):
    queryset = Employ.objects.all()
    serializer_class = EmployPathSerializer
