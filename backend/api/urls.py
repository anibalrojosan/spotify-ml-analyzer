from django.urls import path
from .views import MockAuthView

# Namespace for the API application to avoid naming conflicts
app_name = 'api'

urlpatterns = [
    # This route handles the mock login simulation.
    # POST /api/auth/login/ -> Returns fake user profile & token
    # as_view() converts the class into a function for Django.
    path('auth/login/', MockAuthView.as_view(), name='mock-login'),
]