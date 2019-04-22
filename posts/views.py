from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
from .form import PostForm, ImageForm, CommentForm
from .models import Post, Image, Comment, Hashtag

# Create your views here.
def list(request):
    # 1번
    if request.user.is_authenticated:
        followings = request.user.followings.all()
        posts = Post.objects.filter(Q(user__in=followings) | Q(user = request.user.id)).order_by('-pk')
    else:
        posts = Post.objects.order_by('-pk')
    
    # 2번
    # followings = request.user.followings.all()
    # chain_followings = chain(followings, [request.user])
    # posts = Post.objects.filter(user__in=chain_followings).order_by('-pk')
    
    # posts = Post.objects.filter(user__in=request.user.followings.all()).order_by('-pk')
    # posts = get_list_or_404(Post.objects.order_by('-pk'))
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
            # hashtag / post.content 이후 hashtag 와야함...
            # 1. 게시글을 순회하면서 띄어쓰기를 잘라야함
            # 2. 자른 단어가 #으로 시작 하는지를 판단
            # 3. 해쉬태그가 기존 태그에 있는지?
            for word in post.content.split():
                if word.startswith('#'):
                # if word[0] == '#':
                #     hashtag = Hashtag.objects.get_or_create(content=word)
                #     post.hashtags.add(hashtag[0])
                    try:
                        tag = Hashtag.objects.get(content=word)
                    except ObjectDoesNotExist:
                        tag = Hashtag.objects.create(content=word)
                    post.hashtags.add(tag)

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
                # hashtag update
                post_from.hashtags.clear()
                for word in post_form.content.split():
                    if word.startswith('#'):
                        hashtag = Hashtag.objects.get_or_create(content=word)
                        post_form.hashtags.add(hashtag[0])
                    
                    
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
    
@login_required
def explore(request):
    posts = Post.objects.order_by('-pk')
    # posts = Post.objects.exclude(user=request.user).order_by('-pk')
    form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': form
    }
    return render(request, 'posts/explore.html', context)
    
def hashtag(request, hash_pk):
    tag = get_object_or_404(Hashtag, pk=hash_pk)
    posts = tag.post_set.order_by('-pk')
    context = {
        'hashtag': tag,
        'posts': posts,
    }
    return render(request, 'posts/hashtag.html', context)