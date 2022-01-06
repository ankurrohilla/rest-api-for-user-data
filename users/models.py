from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class User(models.Model):
    _id = models.AutoField(auto_created=True, primary_key=True, serialize=False, editable=False)
    id = models.PositiveSmallIntegerField(unique=True, serialize=True, editable=True, primary_key=False,
                                          verbose_name='ID')
    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    company_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField("ZIP / Postal code", max_length=12)
    email = models.EmailField(unique=True)
    web = models.URLField()
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id', 'age']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
