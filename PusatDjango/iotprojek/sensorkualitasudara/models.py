from django.db import models

# Create your models here.

class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ppm = models.FloatField()
    temp = models.FloatField()
    humi = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} | PPM: {self.ppm} | Temp: {self.temp} | Hum: {self.humi}"
