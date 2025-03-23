from django.db import models

# Create your models here.
class SensorSuhuACData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    ppm = models.FloatField()
    temp = models.FloatField()
    humi = models.FloatField()
    tempout = models.FloatField()
    humiout = models.FloatField()
    tempac = models.FloatField()    
    modeac = models.FloatField()    

    def __str__(self):
        return f"{self.id} | modeac: {self.modeac} | Temp: {self.temp} | Hum: {self.humi} | Tempout: {self.temp} | Humout: {self.humi}"
