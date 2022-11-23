from django.db.models import Q
# Pagination
from django.core.paginator import (
                                        Paginator,
                                        EmptyPage,
                                        PageNotAnInteger, 
                                    )
from posts.models import Post

def paginatePosts(request, objects, per_page):
    page = request.GET.get('page')
    paginator = Paginator(objects, per_page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)
    
    return posts  


def searchCategoryPosts_title(request, queryset=None, category_slug=None):

    search_query = ''
    posts = queryset
    if request.GET.get('search_query') and category_slug is not None:
        search_query = request.GET.get('search_query')
        posts = Post.objects.filter(category__slug__exact=category_slug).distinct().filter(
            Q(title__icontains=search_query) 
            )
        print('search', posts)
    return posts, search_query
        
        