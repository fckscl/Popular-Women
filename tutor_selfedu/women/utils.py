from .models import Category, Women
from django.core.cache import cache

class DataMixin():
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.all()
            cache.set('cats', cats, 60)
        context['cats'] = cats
        context['request'] = self.request
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context