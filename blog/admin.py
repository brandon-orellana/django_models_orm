from django.contrib import admin
from . import models
from .models import Post, Comment

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    readonly_fields = [
        'name',
        'text',
        'email',
    ]

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        #'author',
        #'status',
        'created',
        'updated',
    )

    list_filter = (
        'status',
        'topics',
    )

    prepopulated_fields = {'slug': ('title',)}

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    inlines = [
        CommentInline,
    ]

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )

    prepopulated_fields = {'slug': ('name',)}

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'name',
        'email',
        'created',
        'updated',
        'approved',
    )

    list_filter = (
        'approved',
    )

    search_fields = (
        'post__title',
        'name',
        'email',
        'text',
    )

