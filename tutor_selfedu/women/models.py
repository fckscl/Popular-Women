from django.db import models
from django.urls import reverse

# Create your models here.

class Women(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})
    
    class Meta():
        verbose_name = 'Popular Women'
        verbose_name_plural = 'Popular Women'
        ordering = ['-time_create', 'title']
    
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    
    class Meta():
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id', 'name']
    