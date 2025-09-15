from proxy_imgw.models import Warning
from rest_framework import serializers


class WarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warning
        fields = [
            "id",
            "imgw_id",
            "title",
            "level",
            "possibility",
            "start",
            "end",
            "published",
            "description",
            "comment",
            "office",
            "areas",
            "raw",
            "fetched_at",
        ]


class LocationQuerySerializer(serializers.Serializer):
    lat = serializers.FloatField(required=True)
    lon = serializers.FloatField(required=True)
