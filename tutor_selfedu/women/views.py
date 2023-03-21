from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .forms import *
from .models import *
from .utils import *

# Create your views here.

# menu = ['About', 'Contact', 'Adres', 'Women']

class WomenHome(DataMixin, ListView):

    def get_context_data(self, *, object_list=None, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main Page')
        return {**context, **c_def}
    
    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')

class WomenCategory(DataMixin, ListView):
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        first_post = context["posts"][0]
        c_def = self.get_user_context(title=f'Category {str(first_post.cat)}',
                                      cat_selected=first_post.cat_id)
        return {**context, **c_def}

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

class WomenSearch(DataMixin, ListView):
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        first_post = context["posts"][0]
        context['title'] = f'Results of search'
        context['cat_selected'] = first_post.cat_id
        return context

    def get_queryset(self):
        print(self.request.GET['query'])
        return Women.objects.filter(title__contains=self.request.GET['query'], is_published=True).select_related('cat')


# def index(request):
#     context =  {'title' : 'Main Page',
#                 'menu' : menu,
#                 'cat_selected': 0}

#     return render(request, 'women/index.html', context=context)

def about(request):
    return render(request, 'women/about.html', {'title': 'About App'})

def get(request):
    return HttpResponse(f'{request.GET["name"]}')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = 'home'

    def get_context_data(self, *, object_list=None, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Adding Page')
        return {**context, **c_def}
    
    def form_valid(self, form) -> HttpResponse:
        print(form.cleaned_data)
        return redirect('home')


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Adding Page')
        return {**context, **c_def}

# def add_page(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'title': 'Adding page'})

# def login(request):
#     return HttpResponse("Login")

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get(self, request, *args: any, **kwargs: any) -> HttpResponse:
        Women.objects.filter(slug=kwargs['post_slug']).update(views=F('views')+1)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return {**context, **c_def}
    
# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context =  {'title' : post.title,
#                 'post': post,
#                 'cat_selected': post.cat_id}

#     return render(request, 'women/post.html', context=context)

# def show_category(request, cat_slug):    
#     cat = get_object_or_404(Category, slug=cat_slug)
#     context =  {'title' : 'Women',
#                 'menu' : menu,
#                 'cat_selected': cat.id}
#     return render(request, 'women/index.html', context=context)

def pageNotFound(request, exception):
    return HttpResponseNotFound("404")

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    # success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Register')
        return {**context, **c_def}
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'women/login.html'
    # success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return {**context, **c_def}
    
    def get_success_url(self) -> str:
        return reverse_lazy('home')
    
def logout_user(request):
    logout(request)
    return redirect('login')
