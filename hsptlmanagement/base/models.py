from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    capacity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Bed(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=20)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room.name} - Bed {self.bed_number}"

class Patient(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    disease = models.CharField(max_length=200)
    bed = models.OneToOneField(Bed, on_delete=models.SET_NULL, null=True, blank=True, related_name='patient')
    admitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
