from django.shortcuts import render , get_object_or_404 , redirect
from taggit.models import Tag
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from accounts.models import Profile
# Create your views here.


def home(request):
   
    serach =  request.GET.get('search')
    if serach:
        all_blog = Blog.objects.filter(Q(title__icontains=serach) and Q(content__icontains=serach)).order_by('-id')
    else:
        all_blog = Blog.objects.all().order_by('-id')
        
    page = request.GET.get('page',1) # get page that i will add it soon in html 
    paginator = Paginator(all_blog , 3) # view 3 blogs in one page all_blog is contain all blogs in database now make one page has 3 posts
    try:
      posts= paginator.page(page) # from paginator that i made return the page and it's number that also i made
    except PageNotAnInteger:
        posts = paginator.page(1) # if the number of page is string or anything else return to page 1
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) # if page is empet return lst page from pagintor

    return render(request , 'index.html' , {'all_blog':posts})

def detail_blog(request,pk):
    blog = get_object_or_404(Blog , id = pk)
    comment = Comment.objects.filter(blog = blog , active = True)
    return render(request , 'detail.html' , {'blog':blog , 'comments':comment,})

def get_tag(request,tag_slug):
    all_blog = Blog.objects.all().order_by('-id')
    if tag_slug:
        tag = get_object_or_404(Tag,slug = tag_slug)
        blog = all_blog.filter(tags__in = [tag])
    context = {
        'all_blog':blog,
        'tag':tag,
    }
    return render(request , 'tags.html' , context)

@login_required
def save_comment(request):
    
    if request.method == 'POST':
        pk = request.POST.get('id')
        message = request.POST.get('message')
        blog = get_object_or_404(Blog , id = pk)
        
        new_comment = Comment.objects.create(
            comment = message,
            user = request.user,
            active = True,
            blog = blog
        )
        new_comment.save()
        return redirect('detail_blog' , pk=pk)
    else:
        return render(request, 'error.html', {'error': 'Invalid request method'})

def delete_comment(request):
    if request.POST:
        pk = request.POST.get('id-delete')
        comment = get_object_or_404(Comment , id = pk)
        comment.delete()
        return redirect('detail_blog' , pk = comment.blog.id)
    
def edit_blog(request,pk):
    blog = Blog.objects.get(id=pk)
    if request.POST:
        form = EditBlog(request.POST , request.FILES,instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request , 'Post edited sucsessfully..')
            return redirect('detail_blog',blog.id)
        else:
            messages.warning(request , f"{form.errors}")
    else:
        form = EditBlog(instance=blog)
    return render(request ,'edit_post.html' ,{'form':form , 'blog':blog} )

def delete_blog(request,pk):
    blog = get_object_or_404(Blog , id = pk)
    blog.delete()
    messages.success(request , 'Post deleted sucsessfuly')
    return redirect('home')

@login_required
def create_blog(request):
    if request.POST:
        form = CreateBlog(request.POST , request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            new.save()
            form.save_m2m()
            messages.success(request , 'Post created sucsessfully..')
            return redirect('home')
        else:
            messages.warning(request , f"{form.errors}")
    else:
        form = CreateBlog()
    return render(request , 'create_post.html' , {'form':form})

def about(request):
    profiles = Profile.objects.all()
    about_info = About.objects.all().first
    return render(request , 'about.html',{'about_info':about_info ,'profiles': profiles })

