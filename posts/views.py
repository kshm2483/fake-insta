from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from .form import PostForm, ImageForm, CommentForm
from .models import Post, Image, Comment

# Create your views here.
def list(request):
    posts = get_list_or_404(Post.objects.order_by('-pk'))
    form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': form,
    }
    return render(request, 'posts/list.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect('posts:list')
    else:
        post_form = PostForm()
        image_form = ImageForm()
    context = {
        'post_form': post_form,
        'image_form': image_form,
    }
    return render(request, 'posts/form.html', context)

@login_required
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.user == request.user:
        if request.method == 'POST':
            post_form = PostForm(request.POST, instance=post)
            if post_form.is_valid():
                post_form.save()
                return redirect('posts:list')
        else:
            post_form = PostForm(instance=post)
    else:
        return redirect('posts:list')
    
    context = {
        'post_form': post_form,
        'post': post,
    }
    return render(request, 'posts/form.html', context)

@login_required
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.user == request.user:
        if request.method == "POST":
            post.delete()
            return redirect('posts:list')
    return redirect('posts:list')

@login_required
def create_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.post_id = post_pk
            form.save()
    return redirect('posts:list')
    
@login_required
def delete_comment(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    
    if request.user != comment.user:
        return redirect('posts:list')
        
    if request.method == 'POST':
        comment.delete()
    return redirect('posts:list')
    
@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:list')
    
    # if post.like_users.filter(pk=request.user.pk).exists():
    #     post.like_users.remove(request.user)
    # else:
    #     post.like_users.add(request.user)