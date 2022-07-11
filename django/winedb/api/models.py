from django.db import models

# Create your models here.

class Wine(models.Model):
    class Meta:
        ordering = ['slug']

    # Primary key (url slug from guia penin)
    slug = models.CharField(primary_key=True, max_length=256)
    
    name = models.CharField(max_length=512)
    cellar_name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(blank=True, null=True)
    country = models.CharField(max_length=256)
    zone = models.CharField(max_length=256)
    varieties = models.TextField(blank=True)
    wine_type = models.CharField(blank=True, max_length=256)
    wine_type_simple = models.CharField(blank=True, max_length=256)
    
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ecologic = models.BooleanField()
    penin_points = models.PositiveIntegerField()
    tasting_date = models.DateField(blank=True, null=True)

    style = models.TextField(blank=True)
    mouth = models.TextField(blank=True)
    color = models.TextField(blank=True)
    smell = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.cellar_name}"
