from django.shortcuts import render, redirect, get_list_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
# Pagination and searching bu title
from .utils import searchCategoryPosts_title, paginatePosts

from .models import Category
from posts.models import Post
from posts.utils import postsFilter

def category_posts(request, category_slug):
    category_posts = Post.objects.filter(category__slug=category_slug)
    posts = paginatePosts(request, category_posts, 6)
    posts, filter = postsFilter(request, category_posts)
    # return redirect(reverse('category:category-posts', 
    #                         kwargs={
    #                             'category_slug': category_slug,
    #                             }
    #                         )
    #                 )
    context = {}
    context['posts'] = posts
    context['filter'] = filter
    return render(request, 'index.html', context)


class CategoryPostsList(ListView):
    template_name = 'index.html'
    paginate_by = 5
    
    
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug', '')
        try:
            queryset = Post.objects.filter(category__slug__exact=category_slug).distinct()
        except Post.DoesNotExist:
            queryset = None
            
        return queryset
    
    
    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        category_posts = self.get_queryset()
        if category_posts is not None:
            context = super().get_context_data(**kwargs) 
            _ , context['filter'] = postsFilter(self.request, category_posts)
            context['posts'] = category_posts
            
            # Get a category_slug for the search form in index.html
            category_slug = self.request.path.split('/')[2]
            
            # Search query and filtered posts
            if self.request.GET:
                if self.request.GET.get('search_query'):
                    
                    posts, search_query = searchCategoryPosts_title(
                                                                self.request, 
                                                                category_posts,
                                                                category_slug=category_slug
                                                            )
                    context['search_query'] = search_query
                    print('Search_query ', search_query)
                    
                else:
                    posts, _ = postsFilter(self.request, category_posts)
                context['posts'] = posts
            
            context['category_slug'] = category_slug
            print('Context', context)
            
        return context
     

