from django.urls import path
from .views import CategoryView, ProductListView, ProductDetailView

urlpatterns = [
        path('/category', CategoryView.as_view()),
        path('', ProductListView.as_view()),
        path('/<int:product_id>', ProductDetailView.as_view()),
        # path('/order', FilterView.as_view())
        ]