from django.contrib import admin

from post.models import Post, PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass