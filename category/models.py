from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=250)
    category_image = models.ImageField('image', blank=True, null=True)
    is_listed = models.BooleanField(default=True)
    category_unit = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.category_name
