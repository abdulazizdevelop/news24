from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect 
#from django.views.generic import TemplateView
from django.views.generic import ListView ,CreateView, View, DetailView, UpdateView
from django.views.generic.edit import DeleteView
from .models import News, Category, Tags
from django.urls import reverse_lazy, reverse
from .forms import AddNewForms, Contact_form
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin






    

def list(request):
    cat = request.GET.get('cat')
    qs = News.objects.filter(category__name=cat)
    context = {
        'queryset': qs
    }
    return render(request, 'category_sorts.html', context)


def tags(request):
    tag_kind =request.GET.get('tag')
    qs= News.objects.filter(tags__name=tag_kind)
    context ={
        'queryset': qs
    }
    
    return render(request, 'tags.html', context)


def categorypage(request):
    category = Category.objects.all()
    tags = Tags.objects.all()
    last_news = News.objects.latest("update_at")
    context  ={
        'category' : category,
        'tags' : tags,
        'update_at': last_news
    }
    return render(request, 'index.html', context )

    
class SearchView(ListView):
    template_name = 'search.html'
    model = News
    
    def get_queryset(self): # -> QuerySet[Any]:
        query = self.request.GET.get('search')
        object_list = News.objects.filter(
            Q(title__icontains = query) |Q(body__icontains = query) |Q(category__name__icontains =query)
        )
        
        return object_list
    
    def get_context_data(self, **kwargs: Any): #-> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('search')
        
        return context
    
    class OwnPageprofile(DetailView):
    
        model = News
        template_name = 'profilepage.html'
        context_object_name = 'profile_detail'
        
        def __str__(self) -> str:
            return redirect('home')
            


@login_required

def addnewsview(request):
    if request.POST:
        form = AddNewForms(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            
            form.instance.user = request.user
            form.save()
            
            return redirect('home')

    context= {}
    context['form'] = AddNewForms()
    return render(request, 'add_new.html', context)

def contactpage(request):
    contactForm = Contact_form(request.POST)
    print(contactForm)
    if request.POST and contactForm.is_valid():
        contactForm.save()
        
    
    context= {}
    context['form'] = Contact_form()
    
    return render(request, 'contact.html', context)


class NewsDetailView(DetailView,UserPassesTestMixin,DeleteView):
    
    model = News
    template_name = 'single-page.html'
    context_object_name = 'news_detail'
    
    def test_func(self) -> bool | None:
        obj = self.get_object()  
        return obj.user == self.request.user or  self.request.user.is_superuser
    

    
    

class NewsDeleteView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    
    model = News
    
    template_name = 'news_delate.html'
    
    success_url = reverse_lazy('home')
    
    def test_func(self) -> bool | None:
        obj = self.get_object()  
        return obj.user == self.request.user or  self.request.user.is_superuser
    
    
    
    
    
    
class NewsUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    
    model = News
    form_class = AddNewForms
    template_name = 'news_update.html'
    
    
    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse('news_detail', kwargs={'pk':pk})
    
    
    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.user == self.request.user or self.request.user.is_superuser

def translate_test(request):
    
    return render(request, 'index.html')


def viewnumber(request):
    
   
    viewcount = News.objects.all()
    # viewcount.view_count+=1
    # viewcount.save()
    # print(viewcount)
    context = {
             'vcount' : viewcount
        }
    
    return render(request, 'view.html', context)   
   
def viewnumber2(request ,pk):
    viewcount2 = News.objects.get(id = pk)
    context = {
        'vcount2':viewcount2
    }
    
    return render(request , 'view2.html', context) 

# 1.26
  
    