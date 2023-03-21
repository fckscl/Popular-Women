from django.contrib import admin
from django.urls import reverse_lazy
from .models import *
from django.utils.safestring import mark_safe

# Register your models here.

class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published', 'views', 'women_url')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {'slug':('title',)}
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update', )
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')

    def women_url(self, object):
        return mark_safe(f'<a href={object.get_absolute_url()}>{object.slug}</a>')

    def get_html_photo(self, object: Women):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50>')
        
    get_html_photo.short_description = 'Preview'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)