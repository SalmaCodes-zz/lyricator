from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from models import *
import bcrypt


# Create your views here.

# '/' OR '/main': Shows login/registration page.
def index(request):
    # User.objects.all().delete()
    # Post.objects.all().delete()
    # Version.objects.all().delete()
    # Comment.objects.all().delete()
    return render(request, 'users/index.html')


# '/dashboard': Shows dashboard page.
def dashboard(request):
    if ('user_id' not in request.session.keys()):
        return redirect('/main')

    user = User.objects.get(id=request.session['user_id'])
    popular_posts = Post.objects.annotate(num_stars=Count('starred_by')).order_by("-num_stars")
    context = {
        'user': user,
        'popular_posts': popular_posts
    }
    return render(request, 'users/dashboard.html', context)


# '/dashboard/recent'
def dashboard_recent(request):
    if ('user_id' not in request.session.keys()):
        return redirect('/main')

    user = User.objects.get(id=request.session['user_id'])
    recent_posts = Post.objects.order_by("-created_at")
    context = {
        'user': user,
        'recent_posts': recent_posts
    }
    return render(request, 'users/dashboard_recent.html', context)


# '/posts/new': Shows new post form.
def new_post(request):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'users/new_post.html', context)


# '/posts/create': 'POST' method to create a new post.
def create_post(request):
    if request.method == 'POST':
        errors = Version.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/posts/new')
        else:
            # Create Post
            user = User.objects.get(id=request.session['user_id'])
            post = Post.objects.create(
                title=request.POST['title'],
                type=request.POST['type'],
                owner=user, inspiration=request.POST['inspiration'])
            version = Version.objects.create(
                state=2, #approved
                content=request.POST['content'],
                author=user,
                post=post)
        return redirect('/posts/{}'.format(post.id))


# '/posts/contribute': 'POST' method to handle new contribution submission.
def contribute(request, id):
    if request.method == 'POST':
        errors = Version.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
        else:
            # Create new version
            user = User.objects.get(id=request.session['user_id'])
            post = Post.objects.get(id=id)
            version = Version.objects.create(
                state=1, #pending
                content=request.POST['content'],
                author=user,
                post=post)
        return redirect('/posts/{}'.format(id))


# '/posts/<id>'
def show_post(request, id):
    user = User.objects.get(id=request.session['user_id'])
    post = Post.objects.get(id=id)
    latest_version = post.versions.filter(state=2).last()
    user_pending_versions = post.versions.filter(state=1, author=user)
    owner_pending_versions = post.versions.filter(state=1)
    context = {
        'post': post,
        'post_version': latest_version,
        'user_pending_versions': user_pending_versions,
        'owner_pending_versions': owner_pending_versions,
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'users/show_post.html', context)

# '/posts/<id>/edit'
def edit_post(request, id):
    user = User.objects.get(id=request.session['user_id'])
    post = Post.objects.get(id=id)
    latest_version = post.versions.filter(state=2).last()
    user_pending_versions = post.versions.filter(state=1, author=user)
    owner_pending_versions = post.versions.filter(state=1)
    context = {
        'post': post,
        'post_version': latest_version,
    }
    return render(request, 'users/edit_post.html', context)


# '/posts/edit', POST method
def make_edit_post(request):
    if request.method == 'POST':
        pid = request.POST['pid']
        post = Post.objects.get(id=pid)
        post.title = request.POST['title']
        post.save()
        user = User.objects.get(id=request.session['user_id'])
        version = Version.objects.create(
            state=2, #approved
            content=request.POST['content'],
            author=user,
            post=post)
        return redirect('/posts/{}'.format(post.id))


# '/posts/<id>/v/<vid>'
def show_post_version(request, id, vid):
    post = Post.objects.get(id=id)
    version = Version.objects.get(id=vid)
    context = {
        'post': post,
        'post_version': version,
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'users/show_post.html', context)


# '/posts/v/approve': POST method to approve a version.
def approve_version(request):
    if request.method == 'POST':
        vid = request.POST['vid']
        version = Version.objects.get(id=vid)
        last_version = Version.objects.filter(post=version.post, state=2).last()
        version.content = last_version.content + '\n' + version.content
        version.state = 2
        version.save()
        return redirect('/posts/{}'.format(version.post.id))


# '/posts/v/reject': POST method to reject a version.
def reject_version(request):
    if request.method == 'POST':
        version = Version.objects.get(id=request.POST['vid'])
        version.state = 3
        version.save()
        return redirect('/posts/{}'.format(version.post.id))


# '/posts/star': POST method to star a post.
def star_post(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        post = Post.objects.get(id=request.POST['pid'])
        post.starred_by.add(user)
        return redirect('/posts/{}'.format(post.id))


# '/posts/unstar': POST method to unstar a post.
def unstar_post(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        post = Post.objects.get(id=request.POST['pid'])
        post.starred_by.remove(user)
        return redirect('/posts/{}'.format(post.id))


# '/posts/comment': POST method to comment on a project.
def comment_post(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['user_id'])
        post = Post.objects.get(id=request.POST['pid'])
        content = request.POST['comment']
        comment = Comment.objects.create(
            author=user,
            content=content,
            post=post
        )
        return redirect('/posts/{}'.format(post.id))


# '/users/<id>'
def show_user(request, id):
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'user': User.objects.get(id=id)
    }
    return render(request, 'users/user.html', context)


# Login / Registration / Logout

# '/process': 'POST' method that proccesses the login/registration forms.
def process(request):
    if request.method == 'POST':
        ftype = request.POST['type']
        # Registration form
        if (ftype == 'register'):
            errors = User.objects.registration_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/')
            else:
                # Create User
                password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                user = User.objects.create(
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    username=request.POST['username'],
                    birth_date=request.POST['birth_date'],
                    password=password_hash)
                request.session['user_id'] = user.id
                return redirect('/dashboard')

        # Login form
        elif (ftype == 'login'):
            errors = User.objects.login_validator(request.POST)
            if len(errors):
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
                return redirect('/')
            else: 
                user = User.objects.filter(username=request.POST['username'])
                request.session['user_id'] = user[0].id
                return redirect('/dashboard')
    
# '/logout'
def logout(request):
    request.session.pop('user_id')
    return redirect('/')