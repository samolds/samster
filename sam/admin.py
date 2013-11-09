from django.contrib import admin
from sam.models import *


class TagAdmin(admin.ModelAdmin):
    """ The admin model for an Imager
    """
admin.site.register(Tag, TagAdmin)


class ImageAdmin(admin.ModelAdmin):
    """ The admin model for an Image.
    Content-type, width, and height, are all filled in on Image save.
    """
    exclude = ('content_type', 'width', 'height')
    actions = ['delete_model']

    def get_actions(self, request):
        actions = super(ImageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_model(self, request, queryset):
        if type(queryset) == Image:
            queryset.delete()
        else:
            for image in queryset.all():
                image.delete()
    delete_model.short_description = "Delete selected images"

admin.site.register(Image, ImageAdmin)


class QuoteAdmin(admin.ModelAdmin):
    """ The admin model for a Quote.
    """
    list_filter = ('quote', 'author')
admin.site.register(Quote, QuoteAdmin)


class PostAdmin(admin.ModelAdmin):
    """ The admin model for a Blog Post.
    """
    list_display = ("title",
                    "creation_date",
                    "content")
    list_filter = ["title",
                   "tags",
                   "creation_date",
                   "content"]

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


class ArtAdmin(admin.ModelAdmin):
    """ The admin model for Art.
    """
    list_filter = ('title', 'tags')
admin.site.register(Art, ArtAdmin)
