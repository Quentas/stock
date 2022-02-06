from django.urls import (
    path,
)

from .views import *


urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('products/<category>/', ProductListView.as_view(), name='product'),
]
