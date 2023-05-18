from decimal import Decimal
from rest_framework import viewsets, serializers

from core.models import Dayli
from .utils import BasePathSerializer


class DayliPathSerializer(BasePathSerializer):
    empleado = serializers.StringRelatedField(source="employ")

    @staticmethod
    def get_path():
        return "attendance"

    class Meta:
        model = Dayli
        fields = [
            "employ",
            "empleado",
            "start_at_1",
            "end_at_1",
            "start_at_2",
            "end_at_2",
            "hn",
            "hn_amount",
            "h25",
            "h25_amount",
            "h35",
            "h35_amount",
            "url",
        ]
        extra_kwargs = {
            "employ": {"write_only": True},
            "hn": {"read_only": True},
            "hn_amount": {"read_only": True},
            "h25": {"read_only": True},
            "h25_amount": {"read_only": True},
            "h35": {"read_only": True},
            "h35_amount": {"read_only": True},
        }

    def validate(self, data):
        employ = data.get("employ")
        start_at_1 = data.get("start_at_1")
        end_at_1 = data.get("end_at_1")
        start_at_2 = data.get("start_at_2")
        end_at_2 = data.get("end_at_2")

        diff_time = 0

        if start_at_1 and end_at_1:
            if end_at_1 < start_at_1:
                raise serializers.ValidationError(
                    {"end_at_1": "La fecha/hora no puede ser anterior a la entrada 1"}
                )
            diff_time = end_at_1 - start_at_1

        if start_at_2:
            if not end_at_2:
                raise serializers.ValidationError(
                    {"end_at_2": "No puede ser vacio porque lleno la entrada 2"}
                )

            if start_at_2 < end_at_1:
                raise serializers.ValidationError(
                    {"start_at_2": "La fecha/hora no puede ser anterior a la salida 1"}
                )

            if end_at_2 < start_at_2:
                raise serializers.ValidationError(
                    {"end_at_2": "La fecha/hora no puede ser anterior a la entrada 2"}
                )

            diff_time += end_at_2 - start_at_2
        total_seconds = diff_time.total_seconds()
        total_hours = total_seconds / 3600
        total_hours = Decimal("%0.2f" % round(total_hours, 2))

        cost_per_hour = Decimal("%0.2f" % round(employ.salary / 30 / 8, 3))

        data["hn"] = Decimal(0)
        data["h25"] = 0
        data["h35"] = 0

        if total_hours <= 8:
            data["hn"] = total_hours
            data["hn_amount"] = total_hours * cost_per_hour
        else:
            data["hn"] = 8
            data["hn_amount"] = total_hours * 8
            if total_hours + 2 > 10:
                data["h25"] = 2
                data["h35"] = total_hours - 10
                data["h25_amount"] = round(
                    data["h25"] * cost_per_hour * Decimal(1.25), 2
                )
                data["h35_amount"] = round(
                    data["h35"] * cost_per_hour * Decimal(1.35), 2
                )
            else:
                data["h25"] = total_hours - 8
                data["h25_amount"] = round(
                    data["h25"] * cost_per_hour * Decimal(1.25), 2
                )

        data["total"] = data["hn_amount"] + data["h25_amount"] + data["h35_amount"]
        return data


class DayliViewSet(viewsets.ModelViewSet):
    queryset = Dayli.objects.all()
    serializer_class = DayliPathSerializer
    # ordering_fields = ["empleado", "start_at_1"]

    filterset_fields = {
        "employ__person__name": ["contains"],
        "start_at_1": ["gte"],
        "end_at_1": ["lte"],
    }
