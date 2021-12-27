from django.views.generic import ListView, DetailView, CreateView

from .models import Cheese


class CheeseListView(ListView):
    """View of Cheese list"""
    model = Cheese


class CheeseDetailView(DetailView):
    """View of Cheese Detail"""
    model = Cheese


class CheeseCreateView(CreateView):
    """View of Create Cheese"""
    model = Cheese
    fields = ['name', 'description', 'firmness', 'country_of_origin']
