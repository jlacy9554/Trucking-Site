from . import views
from django.conf.urls import url
from django.urls import path

app = 'Catalog'

urlpatterns = [
    path('driver_catalog/', views.product_list, name='Catalog'),
    path('sponsor_catalog/', views.sponsor_catalog, name='Catalog'),
]

