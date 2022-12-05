from django.db import models
from django.conf import settings

# Create your models here.
class Expense(models.Model):
  CATEGORY_OPTIONS = (
    ('ONLINE_SERVICES', 'ONLINE_SERVICE'),
    ('TRAVEL', 'TRAVEL'),
    ('FOOD', 'FOOD'),
    ('RENT', 'RENT'),
    ('OTHERS', 'OTHERS'),
  )
  category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  description = models.TextField()
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  date = models.DateField(null=True,blank=False)
  
  