from django.urls import path

from business_forms.views import (
    UltimaRequestView, SpasiboUltimaRequestView,
)

urlpatterns = [
    path('spasibo_ultima/', SpasiboUltimaRequestView.as_view(), name='spasibo_ultima'),
    path('', UltimaRequestView.as_view(), name='ultima_form'),
]
