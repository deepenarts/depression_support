from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.urls import path
from django.shortcuts import render


class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'address', 'joined_on')
    search_fields = ('full_name', 'email')

admin.site.register(Patient, PatientAdmin)


user = User.objects.get(username='dipendra')
user.is_staff = True
user.save()


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at',)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor', 'appointment_date', 'status')
    list_filter = ('status', 'doctor')
    search_fields = ('patient_name', 'patient_email', 'doctor__name')
    date_hierarchy = 'appointment_date'

    # Make sure the status field is editable in the list view
    list_editable = ('status',)

admin.site.register(Doctor)
admin.site.register(Appointment, AppointmentAdmin)



class MyAdminSite(admin.AdminSite):
    site_header = "Appointment Management Dashboard"
    site_title = "Admin Dashboard"
    index_title = "Welcome to the Admin Panel"

    def get_urls(self):
        # Add the URL for the custom dashboard
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='custom_dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Fetch appointments and other relevant data for the dashboard
        appointments = Appointment.objects.all().order_by('-appointment_date')[:5]  # Fetch the 5 latest appointments
        total_patients = Appointment.objects.values('patient_email').distinct().count()  # Get total unique patients
        
        context = {
            'appointments': appointments,
            'total_patients': total_patients,
        }
        return render(request, 'admin/dashboard.html', context)

# Register your custom admin site
admin_site = MyAdminSite()


