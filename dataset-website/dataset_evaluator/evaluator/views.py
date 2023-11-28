# evaluator/views.py
import os
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SelectedImage, Batch
from django.db.models import F
from django.conf import settings

image_files = []

def start_page(request):
    submitted_batches = Batch.objects.filter(submitted=True).values_list('batch_number', flat=True)

    # Get a list of image files in the folder
    global image_files
    if not image_files:
        list_dir = sorted(os.listdir(settings.IMAGE_FOLDER))
        image_files = [f for f in list_dir if f.endswith('.jpg')]
    all_batches = range(1, len(image_files) // settings.BATCH_SIZE + 2)  # Assuming you have batches from 1 to 100
    # all_batches = range(1, 404)  # Assuming you have batches from 1 to 100

    context = {
        'submitted_batches': submitted_batches,
        'all_batches': all_batches,
    }
    return render(request, 'start_page.html', context)

def image_grid(request):
    batch_number = int(request.GET.get('batch_number'))
    column_number = int(request.GET.get('column_number'))
    # # Define the path to your images folder
    # images_folder = 'static/images'  # Adjust the folder path as needed

    # # Get a list of image files in the folder
    # image_files = [f for f in os.listdir(images_folder) if f.endswith('.jpg')]
    global image_files

    # Calculate the start and end index for the batch
    start_index = (batch_number - 1) * settings.BATCH_SIZE
    end_index = start_index + settings.BATCH_SIZE
    is_last_batch = end_index >= len(image_files)

    # Slice the image files based on the batch size and number
    batch_images = image_files[start_index:end_index]

    # Generate a list of dictionaries with image information
    images = [{'id': os.path.splitext(image)[0], 'file_path': os.path.join(settings.IMAGE_FOLDER, image)} for image in batch_images]

    return render(request, 'image_grid.html', {'batch_number': batch_number, 
                                               'column_number': column_number, 
                                               'images': images, 
                                               'is_last_batch': is_last_batch})

@csrf_exempt
def save_selected_images(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_ids = data.get('selected_ids', [])
        batch_number = data.get('batch_number', -1)

        print('Selected Images:', selected_ids)

        # Update the SelectedImage model for each selected image
        for image_id in selected_ids:
            selected_image, _ = SelectedImage.objects.get_or_create(image_id=image_id)
            selected_image.selected_count = F('selected_count') + 1
            selected_image.save()

        # Update Batch object for the submitted batch
        batch, _ = Batch.objects.get_or_create(batch_number=batch_number)
        batch.submitted = True
        batch.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})
