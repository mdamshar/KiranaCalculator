from django.db import models
from django.utils.text import slugify

# Create your models here.
class calc(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True, blank=True)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    items = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while calc.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug
        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.name