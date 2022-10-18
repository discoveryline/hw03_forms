from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator

from .models import Group, Post, User


NUMBER_POSTS_PER_PAGE = 10


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(
        post_list, 
        NUMBER_POSTS_PER_PAGE
    ) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(
        post_list, 
        NUMBER_POSTS_PER_PAGE
    ) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)

def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    author_name = author.first_name + ' ' + author.last_name
    # first variant of COUNT - less load on the server
    author_posts_count = len(post_list)
    paginator = Paginator(
        post_list, 
        NUMBER_POSTS_PER_PAGE
    ) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'author_name': author_name,
        'author_posts_count': author_posts_count,
    }
    return render(request, 'posts/profile.html', context)

def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    author_username = post.author
    author = User.objects.get(username=author_username)
    author_name = author.first_name + ' ' + author.last_name
    # second variant of COUNT - less load on the server because no read all posts
    author_posts_count = author.posts.count()
    context = {
        'post': post,
        'author_posts_count': author_posts_count,
    }
    return render(request, 'posts/post_detail.html', context)
