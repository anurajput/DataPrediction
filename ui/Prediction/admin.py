# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import PredictionResult


class PredictionResultAdmin(admin.ModelAdmin):
    list_display = ('date', 'model_number', 'available_qty', 'supply_for_days', 'runs_out_before_next_stock')
admin.site.register(PredictionResult, PredictionResultAdmin)
