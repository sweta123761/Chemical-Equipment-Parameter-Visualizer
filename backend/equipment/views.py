import pandas as pd
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import EquipmentUpload
from .serializers import EquipmentUploadSerializer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


REQUIRED_COLUMNS = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']


def validate_csv(df):
    """Validate that CSV has required columns."""
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    return True, None


def process_csv_data(df):
    """Process CSV data and calculate statistics."""
    # Calculate averages
    avg_flowrate = df['Flowrate'].mean()
    avg_pressure = df['Pressure'].mean()
    avg_temperature = df['Temperature'].mean()
    
    # Calculate equipment type distribution
    equipment_type_dist = df['Type'].value_counts().to_dict()
    
    return {
        'avg_flowrate': round(avg_flowrate, 2),
        'avg_pressure': round(avg_pressure, 2),
        'avg_temperature': round(avg_temperature, 2),
        'equipment_type_distribution': equipment_type_dist,
        'total_records': len(df)
    }


@api_view(['POST'])
@permission_classes([])  # No authentication required
def upload_csv(request):
    """Handle CSV file upload and process data."""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    
    if not file.name.endswith('.csv'):
        return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Read CSV file
        df = pd.read_csv(file)
        
        # Validate CSV
        is_valid, error_message = validate_csv(df)
        if not is_valid:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        # Process data
        stats = process_csv_data(df)
        
        # Create EquipmentUpload instance
        upload = EquipmentUpload.objects.create(
            filename=file.name,
            avg_flowrate=stats['avg_flowrate'],
            avg_pressure=stats['avg_pressure'],
            avg_temperature=stats['avg_temperature'],
            equipment_type_distribution=stats['equipment_type_distribution'],
            total_records=stats['total_records']
        )
        
        # Keep only last 5 uploads
        uploads = EquipmentUpload.objects.order_by('-upload_timestamp')
        if uploads.count() > 5:
            for old_upload in uploads[5:]:
                old_upload.delete()
        
        # Return processed data for visualization
        serializer = EquipmentUploadSerializer(upload)
        response_data = serializer.data
        response_data['raw_data'] = df.to_dict('records')
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([])  # No authentication required
def get_history(request):
    """Return summary of last 5 uploads."""
    uploads = EquipmentUpload.objects.order_by('-upload_timestamp')[:5]
    serializer = EquipmentUploadSerializer(uploads, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([])  # No authentication required
def generate_report(request):
    """Generate PDF report based on analyzed data."""
    upload_id = request.GET.get('id')
    
    if upload_id:
        try:
            upload = EquipmentUpload.objects.get(id=upload_id)
        except EquipmentUpload.DoesNotExist:
            return Response({'error': 'Upload not found'}, status=status.HTTP_404_NOT_FOUND)
        uploads = [upload]
    else:
        # Get most recent upload
        uploads = EquipmentUpload.objects.order_by('-upload_timestamp')[:1]
        if not uploads:
            return Response({'error': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
    
    upload = uploads[0]
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title = Paragraph("Chemical Equipment Parameter Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # File information
    info_data = [
        ['Filename:', upload.filename],
        ['Upload Date:', upload.upload_timestamp.strftime('%Y-%m-%d %H:%M:%S')],
        ['Total Records:', str(upload.total_records)],
    ]
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary statistics
    stats_title = Paragraph("Summary Statistics", styles['Heading2'])
    elements.append(stats_title)
    elements.append(Spacer(1, 0.1*inch))
    
    stats_data = [
        ['Parameter', 'Average Value'],
        ['Flowrate', f"{upload.avg_flowrate}"],
        ['Pressure', f"{upload.avg_pressure}"],
        ['Temperature', f"{upload.avg_temperature}"],
    ]
    stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Equipment type distribution
    dist_title = Paragraph("Equipment Type Distribution", styles['Heading2'])
    elements.append(dist_title)
    elements.append(Spacer(1, 0.1*inch))
    
    dist_data = [['Equipment Type', 'Count']]
    for eq_type, count in upload.equipment_type_distribution.items():
        dist_data.append([eq_type, str(count)])
    
    dist_table = Table(dist_data, colWidths=[3*inch, 3*inch])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(dist_table)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF content
    pdf_content = buffer.getvalue()
    buffer.close()
    
    # Return PDF as response
    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="equipment_report_{upload.id}.pdf"'
    return response
