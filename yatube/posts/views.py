from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.decorators import login_required

from .forms import PostForm

from .models import Group, Post, User

from .utils import paginate_page

POST_PER_PAGE = 10


def index(request):
    post_list = Post.objects.all()
    page_obj = paginate_page(request, post_list, POST_PER_PAGE)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = paginate_page(request, post_list, POST_PER_PAGE)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    page_obj = paginate_page(request, post_list, POST_PER_PAGE)
    context = {
        'page_obj': page_obj,
        'author': author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    # Решил немного не так как Вы сказали
    # Использовал get_object_or_404 для поста, а не для юзера
    # Или Вы это и имели ввиду, а я не понял :)
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    context = {
        'post': post,
        'author': author,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("posts:profile", username=post.author.username)

    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    # Добавил проверку на принадлежнолсть поста автору
    # Мне кажется она нужна, так как через браузер
    # Через инструменты разработчика, можно
    # получить доступ к кнопке "Редаутировать"
    # и присвоить себе чужой пост
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    if author != request.user:
        return redirect("posts:post_detail", post_id)

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("posts:post_detail", post_id)

    context = {
        'form': form,
        'is_edit': True,
    }
    return render(request, 'posts/create_post.html', context)
