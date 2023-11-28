from django.urls import path
from .views import save_selected_images, start_page, image_grid

urlpatterns = [
    path('', start_page, name='start_page'),
    path('image_grid/', image_grid, name='image_grid'),
    path('save_selected_images/', save_selected_images, name='save_selected_images'),
]