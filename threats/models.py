from django.db import models

class Event(models.Model):
    SEVERITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    source_name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['severity']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.severity}"
    
class Alert(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('ACK', 'Acknowledged'),
        ('RESOLVED', 'Resolved'),
    ]

    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="alert")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for Event {self.event.id}"

