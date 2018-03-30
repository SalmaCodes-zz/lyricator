from __future__ import unicode_literals

from django.db import models
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        fname = postData['first_name']
        lname = postData['last_name']
        username = postData['username']
        password = postData['password']
        password_confirmation = postData['password_confirmation']

        # Name - Required; No fewer than 3 characters
        if len(fname) < 3:
            errors["first_name"] = "First Name must be at least 3 characters."
        if len(lname) < 3:
            errors["last_name"] = "Last Name must be at least 3 characters."

        # Username - Required; No fewer than 3 characters; Doesn't already exist
        if len(username) < 3:
            errors["username"] = "Username must be at least 3 characters."
        else:
            data = User.objects.filter(username=username)
            if len(data) > 0:
                errors["username"] = "Username already exists, please log in."
        
        # Password - Required; No fewer than 8 characters in length; matches Password Confirmation
        if len(password) < 8:
            errors["password"] = "Password must be at least 8 characters."
        elif password != password_confirmation:
            errors["password"] = "Password confirmation must match the password."
        return errors
    
    def login_validator(self, postData):
        errors = {}
        username = postData['username']
        password = postData['password']

        data = User.objects.filter(username=username)
        # Username - Required; No fewer than 3 characters;
        if len(username) < 3:
            errors["username"] = "Username must be at least 3 characters."
        
        # Check that the user is registered
        elif len(data) == 0:
            errors["username"] = "Username does not exist. Register first!"
        
        # Make sure the password matches
        elif not bcrypt.checkpw(password.encode(), data[0].password.encode()):
            errors["password"] = "Incorrect password. Try again!"
            
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birth_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} @{}>".format(
            self.name, self.username)


class VersionManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # Item name should be more than 3 chracters
        if len(postData['content']) < 4:
            errors['content'] = "Content should be more than 3 characters."
        return errors


class Post(models.Model):
    type = models.SmallIntegerField() 
    # 1: Lyrics
    # 2: Poem
    # 3: Prose
    # 4: Short Story
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name="posts")
    starred_by = models.ManyToManyField(User, related_name="starred_posts")
    inspiration = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return "<Post object: {}>".format(self.title)


class Version(models.Model):
    state = models.SmallIntegerField(default=1) 
    # 1: Pending (only owner and author can view), 
    # 2: Approved (everyone can view)
    # 3: Rejected (only author can view) 
    content = models.TextField()
    author = models.ForeignKey(User, related_name="versions")
    post = models.ForeignKey(Post, related_name="versions")
    objects = VersionManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return "<Version object: {}>".format(self.content)


# TODO: Comments, Tags
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User,related_name="comments")
    post = models.ForeignKey(Post, related_name="comments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return "<Comment object: {}>".format(self.content)