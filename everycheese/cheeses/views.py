from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cheese


class CheeseListView(ListView):
    """View of Cheese list"""
    model = Cheese


class CheeseDetailView(DetailView):
    """View of Cheese Detail"""
    model = Cheese


class CheeseCreateView(LoginRequiredMixin, CreateView):
    """View of Create Cheese"""
    model = Cheese
    fields = ['name', 'description', 'firmness', 'country_of_origin']

    def form_valid(self, form):
        """Form validation for Add Cheese form."""
        form.instance.creator = self.request.user
        return super().form_valid(form)
