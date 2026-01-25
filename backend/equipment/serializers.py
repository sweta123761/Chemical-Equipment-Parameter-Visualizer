from rest_framework import serializers
from .models import EquipmentUpload


class EquipmentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentUpload
        fields = ['id', 'filename', 'upload_timestamp', 'avg_flowrate', 
                  'avg_pressure', 'avg_temperature', 'equipment_type_distribution', 
                  'total_records']
        read_only_fields = ['id', 'upload_timestamp']
