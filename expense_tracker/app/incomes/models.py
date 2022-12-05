from django.db import models
from django.conf import settings

# Create your models here.
class Income(models.Model):
  SOURCE_OPTIONS = (
    ('SALARY', 'SALARY'),
    ('BUSINESS', 'BUSINESS'),
    ('SIDE-HUSTLE', 'SIDE-HUSTLE'),
    ('OTHERS', 'OTHERS'),
  )

  source = models.CharField(choices=SOURCE_OPTIONS, max_length=255)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField()
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  date = models.DateField(null=True, blank=False)
  