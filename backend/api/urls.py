from django.urls import path
from api.views import MockLoginView, MeView

urlpatterns = [
    path('auth/mock-login/', MockLoginView.as_view(), name='mock-login'),
    path('auth/me/', MeView.as_view(), name='me'),
]
