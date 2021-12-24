from django.views.generic import ListView, DetailView

from .models import Cheese


class CheeseListView(ListView):
    """View of Cheese list"""
    model = Cheese


class CheeseDetailView(DetailView):
    """View of Cheese Detail"""
    model = Cheese
