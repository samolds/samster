from django.contrib import admin
from sam.models import *


class TagAdmin(admin.ModelAdmin):
    """ The admin model for an Tag
    """
admin.site.register(Tag, TagAdmin)


class SiteImageAdmin(admin.ModelAdmin):
    """ The admin model for an SiteImage.
    Content-type, width, and height, are all filled in on Image save.
    """
    exclude = ('content_type', 'width', 'height')
    actions = ['delete_model']

    def get_actions(self, request):
        actions = super(SiteImageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_model(self, request, queryset):
        if type(queryset) == SiteImage:
            queryset.delete()
        else:
            for image in queryset.all():
                image.delete()
    delete_model.short_description = "Delete selected images"

admin.site.register(SiteImage, SiteImageAdmin)


class QuoteAdmin(admin.ModelAdmin):
    """ The admin model for a Quote.
    """
    list_filter = ('quote', 'author')
admin.site.register(Quote, QuoteAdmin)


class CommentAdmin(admin.ModelAdmin):
    """ The admin model for a Comment.
    """
    list_display = ("name",
                    "subject",
                    "email",
                    "date")
    list_filter = ["name",
                   "email",
                   "date"]

    actions = ['delete_model']

    def get_actions(self, request):
        actions = super(CommentAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_model(self, request, comments):
        if type(comments) is Comment:
            comments.delete()
        else:
            for comment in comments.all():
                comment.delete()
    delete_model.short_description = "Delete selected commentss"

admin.site.register(Comment, CommentAdmin)


class PostAdmin(admin.ModelAdmin):
    """ The admin model for a Blog Post.
    """
    list_display = ("title",
                    "creation_date")
    list_filter = ["title",
                   "tags",
                   "creation_date"]

    actions = ['delete_model']

    def get_actions(self, request):
        actions = super(PostAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_model(self, request, posts):
        if type(posts) is Post:
            posts.delete()
        else:
            for post in posts.all():
                post.delete()
    delete_model.short_description = "Delete selected posts"

admin.site.register(Post, PostAdmin)
