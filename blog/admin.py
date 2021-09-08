from django.contrib import admin

from .models import Comment, Post, Author, Tag
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_filter = ('tags', 'author', 'date')
    list_display = ('title', 'author', 'date')

    prepopulated_fields = {
        "slug": ('title',)
    }


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'post')


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
