from django.views import generic
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView ,UpdateView ,DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import PredictionResult
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from .filters import UserFilter


def results(request):
    print "Getting results"
    item_list = PredictionResult.objects.all()
    item_filter = UserFilter(request.GET, queryset=item_list)
    return render(request, 'Prediction/index.html', {'filter': item_filter})


class IndexView(generic.ListView):

    template_name = 'Prediction/index.html'
    context_object_name = 'show_result'
    paginate_by = 50

    def get_queryset(self):
        return PredictionResult.objects.all()
