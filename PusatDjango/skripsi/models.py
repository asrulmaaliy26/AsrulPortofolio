from django.db import models

# Create your models here.
class SensorSmartACData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    tempout = models.FloatField()
    humiout = models.FloatField()
    tempac = models.FloatField()    
    modeac = models.FloatField()    
    hasilpred = models.FloatField()    

    def __str__(self):
        return f"{self.id} | Hasil Prediksi {self.hasilpred}"
