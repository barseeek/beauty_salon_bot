from django.db import models
from django.contrib.auth.models import AbstractUser


class Salon(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Master(AbstractUser):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.last_name} {self.first_name} - {self.salon.name}"


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    length = models.TimeField()

    def __str__(self):
        return self.name


class Appointment(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} - {self.service.name} - {self.appointment_time}"


class Schedule(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.salon.name} - {self.master.username} - {self.date} {self.start_time}-{self.end_time}"
