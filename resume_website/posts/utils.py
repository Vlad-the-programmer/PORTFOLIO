from .models import Post, Tags
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginatePosts(request, posts, results):

    page = request.GET.get('page')
    paginator = Paginator(posts, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, posts


def searchPosts(request, queryset=None):

    search_query = ''
    posts = queryset
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

        tags = Tags.objects.filter(title__icontains=search_query)

        posts = Post.objects.distinct().filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            # Q(owner__name__icontains=search_query) |
            Q(tags__in=tags)
        )
    
    return posts, search_query