# evaluator/views.py
import os
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SelectedImage
from django.db.models import F

def start_page(request):
    return render(request, 'start_page.html')

def image_grid(request):
    batch_number = int(request.GET.get('batch_number'))
    # Define the path to your images folder
    images_folder = 'static/images'  # Adjust the folder path as needed

    # Get a list of image files in the folder
    image_files = [f for f in os.listdir(images_folder) if f.endswith('.jpg')]

    # Set the batch size
    batch_size = 17  # Adjust the batch size as needed

    # Calculate the start and end index for the batch
    start_index = (batch_number - 1) * batch_size
    end_index = start_index + batch_size
    is_last_batch = end_index >= len(image_files)

    # Slice the image files based on the batch size and number
    batch_images = image_files[start_index:end_index]

    # Generate a list of dictionaries with image information
    images = [{'id': os.path.splitext(image)[0], 'file_path': os.path.join(images_folder, image)} for image in batch_images]

    return render(request, 'image_grid.html', {'batch_number': batch_number, 'images': images, 'is_last_batch': is_last_batch})

@csrf_exempt
def save_selected_images(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_ids = data.get('selected_ids', [])

        print('Selected Images:', selected_ids)

        # Update the SelectedImage model for each selected image
        for image_id in selected_ids:
            selected_image, created = SelectedImage.objects.get_or_create(image_id=image_id)
            if not created:
                # If the image already exists, increment the selected_count
                selected_image.selected_count = F('selected_count') + 1
                selected_image.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})
