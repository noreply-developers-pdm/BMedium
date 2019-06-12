from django.shortcuts import render, redirect
from .models import Post
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm


# import filters


# Create your views here.


def home(request):
    total_users = User.objects.all().count()
    posts = Post.objects.all()
    total_posts_count = Post.objects.all().count()

    context = {'posts': posts,
               'total_users': total_users,
               'total_posts_count': total_posts_count}
    return render(request, "posts.html", context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account for {username} has been created Successfully')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)


@login_required
def profile(request, username):
    user = User.objects.get(username=request.user)
    user_posts = user.myapp_posts.all()
    user_posts_count = user.myapp_posts.all().count()
    # user_posts = UserFilter(request.GET, queryset=posts)
    return render(request, 'registration/profile.html', {'posts': user_posts, 'u_p_count': user_posts_count}, username)


@login_required
def add_posts(request, username):
    return render(request, 'add_posts.html', {}, username)


def add_posts_submit(request):
    if request.method == 'POST':
        post_title = request.POST.get('title')
        post_content = request.POST.get('content')
        post_author_id = request.POST.get('author_id')
        try:
            form = Post(title=post_title, content=post_content, author_id=post_author_id)
            form.save()
            messages.success(request, f'Post has been Successfully Added!')
        except Exception as e:
            print(e)
    else:
        # return render(request, '404.html')
        return redirect('error_404')
    return redirect('blog-home')


# class UserFilter(filters.FieldSet):
#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'date_posted', 'author']

def delete_posts(request):
    if request.method == 'POST':
        del_post_of_id = request.POST.get('del_post_of_id')
        # resolved deleting of post with same title names, and assign filter to 'post id' instead, as it's always unique
        Post.objects.filter(id=del_post_of_id).delete()
        messages.success(request, f'Your Post has been Deleted!')
    else:
        return redirect('error_404')
    return redirect('profile')


def update_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        update_title_to = request.POST.get('update_title_to')
        update_content_to = request.POST.get('update_content_to')
        Post.objects.filter(id=post_id).update(title=update_title_to, content=update_content_to)
        messages.success(request, f'Your Post has been Updated!')
    else:
        return redirect('error_404')
    return redirect('profile')


def error_404(request):
    return render(request, "404.html")


def full_post(request, pid, title):
    all_post = Post.objects.all()
    for x in all_post:
        list_p_title = x.title
        list_pid = x.id
    if request.method == 'POST':
        current_post_id = request.POST.get('idd')
        # getting current post_id from post request so that current post with that id will be shown up on full_post.html
        posts = Post.objects.filter(id=current_post_id)
        context = {
            'posts': posts,
            'current_post_id': current_post_id
        }
        print('post request done')
        return render(request, 'full_post.html', context)
    else:
        current_post_id = pid
        current_post_title = title
        # print(title)
        print(current_post_id)
        print("NO Post request")

        posts = Post.objects.filter(id=current_post_id, title=current_post_title)

        if current_post_id == list_pid and current_post_title == list_p_title:
            context = {
                'posts': posts,
                'current_post_id': current_post_id
            }
            return render(request, 'full_post.html', context)
        else:
            # return redirect('error_404')
            return render(request, '404.html', {})
