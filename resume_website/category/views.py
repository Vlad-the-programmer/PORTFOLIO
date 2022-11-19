from django.shortcuts import render, redirect, get_list_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
# Pagination
from .utils import paginatePosts
from .utils import searchCategoryPosts

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
            queryset = Post.objects.filter(category__slug=category_slug).distinct()
        except Post.DoesNotExist:
            queryset = None
            
        return queryset
    
    
    def get(self, request, *args, **kwargs):
        self.request = request
        return super().get(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        category_posts = self.get_queryset()
        # print(category_posts)
        if category_posts is not None:
            context = super().get_context_data(**kwargs) 
            
            # Get a category_slug for the search form in index.html
            category_slug = self.request.path.split('/')[2]
            
            # Search query and filtered posts
            search_query = ''
            if self.request.GET.get('search_query'):
                posts, search_query = searchCategoryPosts(
                                                            self.request, 
                                                            category_posts,
                                                            category_slug=category_posts
                                                        )
                context['posts'] = posts
                print('Search_query ', search_query)
            else:    
                posts, filter = postsFilter(self.request, category_posts)
                context['filter'] = filter
                context['posts'] = posts
                
                
            print(posts)
            print('Context', context)
            context['category_slug'] = category_slug
            context['search_query'] = search_query
            
        else:   
            context = {}
        return context
     

