from django import forms
from django.contrib.auth.models import User
from .models import Patient, Blog, Appointment

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['full_name', 'email', 'address', 'profile_image']



class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'patient_email', 'doctor', 'appointment_date']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={
                'placeholder': '2025-02-22T13:25',
                'type': 'datetime-local',  # DateTime input for browser date-picker
            }),
        }