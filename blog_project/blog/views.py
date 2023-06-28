from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView

from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm

from django.contrib.auth.decorators import login_required

def home(request):
    posts = BlogPost.objects.all().order_by('-date_posted')
    context = {
        'posts': posts,
        'user': request.user,
        'form': BlogPostForm()
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        form.author = request.user
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('home') 
        else:
            print(form.errors)
    else:
        form = BlogPostForm()


    return redirect('home')

@login_required
def delete_post(request, post_id):
    # Retrieve the blog post object
    try:
        post = BlogPost.objects.get(pk=post_id)
    except BlogPost.DoesNotExist:
        return redirect('home')

    # Check if the logged-in user is the author of the post
    if post.author != request.user:
        return redirect('home')

    # Delete the post
    post.delete()
    return redirect('home')

@login_required
def add_comment(request, post_id):
    # Retrieve the blog post object
    try:
        post = BlogPost.objects.get(pk=post_id)
    except BlogPost.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'form': form
    }
    return render(request, 'add_comment.html', context)

@login_required
def delete_comment(request, comment_id):
    # Retrieve the comment object
    try:
        comment = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return redirect('home')

    # Check if the logged-in user is the author of the comment
    if comment.author != request.user:
        return redirect('home')

    # Delete the comment
    comment.delete()
    return redirect('home')

class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse('home')

class CustomLogoutView(LogoutView):
    def get_success_url(self):
        return reverse('home')
