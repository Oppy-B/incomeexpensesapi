from django.db import models
from django.db.models.deletion import CASCADE
from authentication.models import User
# Create your models here.

class Expenses(models.Model):
    CATEGORY_OPTIONS = [
        ('ONLINE_SERVICE','ONLINE_SERVICE'),
        ('TRAVEL','TRAVEL'),
        ('FOOD','FOOD'),
        ('RENT','RENT'),
        ('OTHERS','OTHERS')
    ]

    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=CASCADE)
    date = models.DateField(null=False, blank=False)
    
    class Meta:
        ordering = ['-date']

    def __str__(self) -> str:
        return str(self.owner) + '\'s income'

