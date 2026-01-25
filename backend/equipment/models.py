from django.db import models
from django.utils import timezone
import json


class EquipmentUpload(models.Model):
    """Model to store metadata of CSV uploads."""
    filename = models.CharField(max_length=255)
    upload_timestamp = models.DateTimeField(default=timezone.now)
    
    # Summary statistics stored as JSON
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    
    # Equipment type distribution stored as JSON
    equipment_type_distribution = models.JSONField()
    
    # Total number of records
    total_records = models.IntegerField()
    
    class Meta:
        ordering = ['-upload_timestamp']
    
    def __str__(self):
        return f"{self.filename} - {self.upload_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
