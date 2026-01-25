from django.contrib import admin
from .models import EquipmentUpload


@admin.register(EquipmentUpload)
class EquipmentUploadAdmin(admin.ModelAdmin):
    list_display = ['filename', 'upload_timestamp', 'total_records', 'avg_flowrate', 'avg_pressure', 'avg_temperature']
    list_filter = ['upload_timestamp']
    readonly_fields = ['upload_timestamp']
