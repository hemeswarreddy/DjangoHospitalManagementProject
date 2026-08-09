from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Bed, Patient
from .serializers import RoomSerializer, BedSerializer, PatientSerializer

def rooms_page(request):
    return render(request, 'base/rooms.html')

# --- Room ---
@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    return Response(RoomSerializer(rooms, many=True).data)

@api_view(['POST'])
def add_room(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_room(request, pk):
    Room.objects.get(id=pk).delete()
    return Response({'message': 'Room deleted'}, status=status.HTTP_204_NO_CONTENT)

# --- Bed ---
@api_view(['GET'])
def get_beds(request, room_id):
    beds = Bed.objects.filter(room_id=room_id)
    return Response(BedSerializer(beds, many=True).data)

@api_view(['POST'])
def add_bed(request, room_id):
    data = request.data.copy()
    data['room'] = room_id
    serializer = BedSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_bed(request, pk):
    Bed.objects.get(id=pk).delete()
    return Response({'message': 'Bed deleted'}, status=status.HTTP_204_NO_CONTENT)

# --- Patient ---
@api_view(['GET'])
def get_patients(request):
    patients = Patient.objects.select_related('bed__room').all()
    return Response(PatientSerializer(patients, many=True).data)

@api_view(['GET'])
def get_room_patients(request, room_id):
    patients = Patient.objects.select_related('bed').filter(bed__room_id=room_id)
    return Response(PatientSerializer(patients, many=True).data)

@api_view(['POST'])
def allocate_bed(request):
    name = request.data.get('name')
    age = request.data.get('age')
    disease = request.data.get('disease')
    room_id = request.data.get('room_id')

    bed = Bed.objects.filter(room_id=room_id, is_available=True).first()
    if not bed:
        return Response({'error': 'No available beds in this room'}, status=status.HTTP_400_BAD_REQUEST)

    patient = Patient.objects.create(name=name, age=age, disease=disease, bed=bed)
    bed.is_available = False
    bed.save()
    return Response(PatientSerializer(patient).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def discharge_patient(request, pk):
    patient = Patient.objects.get(id=pk)
    if patient.bed:
        patient.bed.is_available = True
        patient.bed.save()
    patient.delete()
    return Response({'message': 'Patient discharged and bed freed'})
