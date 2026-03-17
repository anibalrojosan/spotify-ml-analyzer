from django.urls import path
from api.views import MockLoginView

urlpatterns = [
    path('auth/mock-login/', MockLoginView.as_view(), name='mock-login'),
]
