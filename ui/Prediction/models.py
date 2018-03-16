from django.db import models
from django.core.urlresolvers import reverse
#from datetime import datetime

class PredictionResult(models.Model):
    class Meta:
        db_table = 'prediction_results'

    date            = models.CharField(max_length=250)
    model_number    = models.CharField(max_length=500)
    available_qty   = models.IntegerField()
    supply_for_days = models.IntegerField()
    runs_out_before_next_stock = models.CharField(max_length=1000)

    def get_absolute_url(self):
        return reverse('Prediction:index',kwargs={'pk':self.pk})

    def __str__(self):
        return self.model_number

    def __unicode__(self):
        return self.model_number
