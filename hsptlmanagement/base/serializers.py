from rest_framework import serializers
from .models import Room, Bed, Patient

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class BedSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.name', read_only=True)
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = Bed
        fields = ['id', 'room', 'room_name', 'bed_number', 'is_available', 'patient_name']

    def get_patient_name(self, obj):
        return obj.patient.name if hasattr(obj, 'patient') and obj.patient else None

class PatientSerializer(serializers.ModelSerializer):
    bed_info = BedSerializer(source='bed', read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'name', 'age', 'disease', 'bed', 'bed_info', 'admitted_at']
