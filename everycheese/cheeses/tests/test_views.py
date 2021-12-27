import pytest
from pytest_django.asserts import (
    assertContains,
    assertRedirects,
)

from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from everycheese.users.models import User
from ..models import Cheese
from ..views import (
    CheeseCreateView,
    CheeseListView,
    CheeseDetailView
)
from .factories import CheeseFactory

pytestmark = pytest.mark.django_db


def test_good_cheese_list_view(rf):
    """Test Cheese List View"""
    # Get the request
    request = rf.get(reverse('cheeses:list'))
    # User the request to get the response
    response = CheeseListView.as_view()(request)
    # Test that the response is valid
    assertContains(response, 'Cheese list')


def test_good_cheese_detail_view(rf):
    """Test Cheese Detail view."""
    cheese = CheeseFactory()
    url = reverse('cheeses:detail',
                  kwargs={'slug': cheese.slug})
    request = rf.get(url)
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    assertContains(response, cheese.name)


def test_good_cheese_create_view(rf, admin_user):
    """Test Add Cheese view."""
    cheese = CheeseFactory()
    request = rf.get(reverse('cheeses:add'))

    request.user = admin_user
    response = CheeseCreateView.as_view()(request)

    assert response.status_code == 200


def test_cheese_list_contains_2_cheeses(rf):
    """Test that Cheese List view contains cheeses"""
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()

    request = rf.get(reverse('cheeses:list'))
    response = CheeseListView.as_view()(request)

    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)


def test_detail_contains_cheese_data(rf):
    """Test that Cheese Detail view contains cheese data"""
    cheese = CheeseFactory()
    url = reverse('cheeses:detail',
                  kwargs={'slug': cheese.slug})
    request = rf.get(url)

    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)

    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)


def test_cheese_create_form_valid(rf, admin_user):
    """Test successful submission of Cheese form"""
    form_data = {
        'name': 'Paski Sir',
        'description': 'A salty hard cheese',
        'firmness': Cheese.Firmness.HARD
    }
    request = rf.post(reverse('cheeses:add'), form_data)
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)

    cheese = Cheese.objects.get(name='Paski Sir')

    assert cheese.description == form_data['description']
    assert cheese.firmness == form_data['firmness']
    assert cheese.creator == admin_user
