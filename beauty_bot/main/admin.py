from django.contrib import admin
from main.models import Salon, Master, Schedule, Service, Appointment


admin.site.register(Salon)
admin.site.register(Master)
admin.site.register(Schedule)
admin.site.register(Service)
admin.site.register(Appointment)