from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class calc(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receipts')
    name = models.CharField(max_length=60)
    slug = models.SlugField(blank=True)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    items = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['user', 'slug']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while calc.objects.filter(user=self.user, slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug
        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.name