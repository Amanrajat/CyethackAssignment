from rest_framework import serializers
from .models import Event, Alert

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ['timestamp']


class AlertSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = "__all__"
        read_only_fields = ['created_at']
