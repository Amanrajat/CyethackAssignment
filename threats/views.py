# threats/views.py
from rest_framework import viewsets
from .models import Event, Alert
from .serializers import EventSerializer , AlertSerializer
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        event = serializer.save()
        if event.severity in ['HIGH', 'CRITICAL']:
            Alert.objects.create(event=event)



class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.select_related('event')
    serializer_class = AlertSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'event__severity']

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAdminUser()]
        return super().get_permissions()