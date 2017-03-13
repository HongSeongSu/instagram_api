from django.contrib import admin

# Register your models here.
from post.models import Post, PostPhoto

admin.site.register(Post)
admin.site.register(PostPhoto)
