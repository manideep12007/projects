from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Post,Category
from .forms import PostForm,CategoryForm
from django.http import HttpResponseNotFound

# listing all the records 
def listviews(request):
    category_id = request.GET.get('category')
    if category_id:
        posts = Post.objects.filter(category__id=category_id).order_by('-updated')
    else:
        posts = Post.objects.all().order_by('-updated')
    categories = Category.objects.all()
    context = {
        'posts':posts,'categories':categories,
    }
    return render(request,'home.html',context)

# create post 
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:home')
    else:
        form = PostForm()
    context = {
        'form':form
    }
    return render(request,'create.html',context)

# update form 
@login_required
def update_post(request,post_id):
    try:
        post = Post.objects.get(pk=post_id,author=request.user)
    except Post.DoesNotExist:
        return HttpResponseNotFound(f'no post on post id {post_id} ')
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:home')
    else:
        form = PostForm(instance=post)
    context = {
        'form':form
    }
    return render(request,'create.html',context)

# delete post
@login_required
def delete_post(request,post_id):
    try:
        post = Post.objects.get(pk=post_id,author=request.user)
    except Post.DoesNotExist:
        return HttpResponseNotFound(f'no post on post id {post_id} ')
    if request.method == 'POST':
        post.delete()
        return redirect(request,'blog:home')
    context = {
        'post':post
    }
    return render(request,'delete.html',context)

#new category creation
@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:home')
    else:
        form = CategoryForm()
    context = {'form':form}
    return render(request,'create_category.html',context)  