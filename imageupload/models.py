from django.db import models

class image(models.Model):
    photo = models.ImageField(upload_to="images")
