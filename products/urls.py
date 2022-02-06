from django.urls import (
    path,
    include
)
from .views import (
    CategoryListView,
    ProductListView
)


urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('products/<category>/', ProductListView.as_view(), name='product'),
]
