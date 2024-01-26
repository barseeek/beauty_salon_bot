from django.db import models


class Salon(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Client(models.Model):
    fullname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    tg_id = models.CharField(max_length=50)

    def __str__(self):
        return self.fullname


class Master(models.Model):
    fullname = models.CharField(max_length=255)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='masters')

    def __str__(self):
        return f"{self.fullname} - {self.salon.name}"


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    length = models.TimeField()

    def __str__(self):
        return self.name


class Appointment(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='appointments')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    appointment_time = models.DateTimeField()

    def __str__(self):
        return f"{self.client.fullname} - {self.service.name} - {self.appointment_time}"


class Schedule(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.master.salon.name} - {self.master.fullname} - {self.date} {self.start_time}-{self.end_time}"
