import argparse
import csv
import os
import django
# from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dataset_evaluator.settings')
django.setup()

# # Configure the Django settings
# settings.configure(
#     DATABASES={
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': 'db.sqlite3',
#         }
#     },
#     INSTALLED_APPS=[
#         'dataset_evaluator',
#         # Add other installed apps here
#     ],
# )

from evaluator.models import SelectedImage

def save_selected_images_to_csv(file_path='selected_images.csv'):
    selected_images = SelectedImage.objects.all()

    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['image_id', 'selected_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for image in selected_images:
            writer.writerow({
                'image_id': image.image_id,
                'selected_count': image.selected_count,
            })

    print(f'Selected images saved to {file_path}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Save SelectedImage dataset to a CSV file.')
    parser.add_argument('--file', help='Path to the CSV file (default: selected_images.csv)', default='selected_images.csv')

    args = parser.parse_args()
    save_selected_images_to_csv(file_path=args.file)
