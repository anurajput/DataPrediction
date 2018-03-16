from .models import PredictionResult
import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = PredictionResult
        fields = ['date', 'available_qty', 'model_number', 'supply_for_days', 'runs_out_before_next_stock']
