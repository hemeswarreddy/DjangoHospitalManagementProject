from django.urls import path
from . import views

urlpatterns = [
    path('', views.rooms_page, name='rooms'),
    path('rooms/', views.get_rooms),
    path('rooms/add/', views.add_room),
    path('rooms/update/<str:pk>/', views.update_room),
    path('rooms/delete/<str:pk>/', views.delete_room),
    path('rooms/<int:room_id>/beds/', views.get_beds),
    path('rooms/<int:room_id>/beds/add/', views.add_bed),
    path('rooms/<int:room_id>/patients/', views.get_room_patients),
    path('beds/delete/<int:pk>/', views.delete_bed),
    path('patients/', views.get_patients),
    path('patients/allocate/', views.allocate_bed),
    path('patients/discharge/<int:pk>/', views.discharge_patient),
]
