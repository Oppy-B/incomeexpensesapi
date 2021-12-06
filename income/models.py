from django.db import models
from django.db.models.deletion import CASCADE
from authentication.models import User
# Create your models here.

class Income(models.Model):
    SOURCE_OPTIONS = [
        ('SALARY','SALARY'),
        ('BUISNESS','BUISNESS'),
        ('SIDE-HUSTLES','SIDE-HUSTLES'),
        ('OTHERS','OTHERS')
    ]

    source = models.CharField(choices=SOURCE_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=CASCADE)
    date = models.DateField(null=False, blank=False)
    
    class Meta:
        ordering = ['-date']

    def __str__(self) -> str:
        return str(self.owner) + '\'s income'