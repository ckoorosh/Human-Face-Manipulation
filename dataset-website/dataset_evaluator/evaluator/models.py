from django.db import models

class SelectedImage(models.Model):
    image_id = models.CharField(unique=True, max_length=16)
    selected_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Image {self.image_id}"

class Batch(models.Model):
    batch_number = models.IntegerField(unique=True)
    submitted = models.BooleanField(default=False)