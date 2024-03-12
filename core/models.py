from django.db import models

class Blogs(models.Model):
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()

class Chats(models.Model):
    chat_id = models.AutoField(primary_key=True)
    from_id = models.IntegerField()
    to_id = models.IntegerField()
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    sender_id = models.IntegerField()
    participants_id = models.IntegerField()
    conversation_id = models.IntegerField()

class Cities(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

class Comment(models.Model):
    chat_id = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()

class Conversations(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.IntegerField()

class Follows(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    following_user_id = models.IntegerField()
    followed_user_id = models.IntegerField()
    time = models.DateTimeField(null=True)

class Friend(models.Model):
    friend_id = models.AutoField(primary_key=True)
    friend_id_1 = models.IntegerField()
    friend_id_2 = models.IntegerField()
    time = models.DateTimeField()

class Likes(models.Model):
    like_id = models.AutoField(primary_key=True)
    chat_id = models.IntegerField()
    blogs_id = models.IntegerField()
    user_id = models.IntegerField()
    time = models.DateTimeField()
