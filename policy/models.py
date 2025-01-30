from django.db import models
import uuid
# Create your models here.
class Policy(models.Model):
    TYPE_CHOICES = [
        ('Term Life', 'Term Life'),
        ('Health', 'Health'),
        ('Vehicle', 'Vehicle'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    coverage = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'policy'
        ordering = ['-created_at']  
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'


