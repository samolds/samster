from django.contrib import admin
from django.forms import TextInput, Textarea, SelectMultiple
from django.db import models
from sam.models import *


class TagAdmin(admin.ModelAdmin):
    """ The admin model for a Tag
    """
admin.site.register(Tag, TagAdmin)


class WebsiteAdmin(admin.ModelAdmin):
    """ The admin model for a Website
    """
    list_display = ("display",
                    "url",
                    "kind",
                    "private")
    list_filter = ["private", "kind"]
    actions = ["mark_private",
               "mark_public"]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'168'})},
        models.TextField: {'widget': Textarea(attrs={'rows':40, 'cols':120})},
        models.ManyToManyField: {'widget': SelectMultiple(attrs={'size':'15'})}
    }

    def mark_private(self, request, queryset):
        if type(queryset) == Website:
            queryset.private = True
            queryset.save()
        else:
            for site in queryset.all():
                site.private = True
                site.save()
    mark_private.short_description = "Mark selected as private"

    def mark_public(self, request, queryset):
        if type(queryset) == Website:
            queryset.private = False
            queryset.save()
        else:
            for site in queryset.all():
                site.private = False
                site.save()
    mark_public.short_description = "Mark selected as public"


admin.site.register(Website, WebsiteAdmin)


class SiteImageAdmin(admin.ModelAdmin):
    """ The admin model for a SiteImage.
    Content-type, width, and height, are all filled in on Image save.
    """
    list_filter = ["private",
                   "tags",
                   "creation_date"]
    list_display = ("name", "private")
    exclude = ('content_type', 'width', 'height', 'comments',)
    readonly_fields = ('view_count', 'description',)
    actions = ["mark_private",
               "mark_public",
               "delete_model"]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'168'})},
        models.TextField: {'widget': Textarea(attrs={'rows':40, 'cols':120})},
        models.ManyToManyField: {'widget': SelectMultiple(attrs={'size':'15'})}
    }

    def mark_private(self, request, queryset):
        if type(queryset) == SiteImage:
            queryset.private = True
            queryset.save()
        else:
            for image in queryset.all():
                image.private = True
                image.save()
    mark_private.short_description = "Mark selected as private"

    def mark_public(self, request, queryset):
        if type(queryset) == SiteImage:
            queryset.private = False
            queryset.save()
        else:
            for image in queryset.all():
                image.private = False
                image.save()
    mark_public.short_description = "Mark selected as public"

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
    delete_model.short_description = "Delete selected Images"

admin.site.register(SiteImage, SiteImageAdmin)


class QuoteAdmin(admin.ModelAdmin):
    """ The admin model for a Quote.
    """
    list_filter = ['private', 'tags', 'author']
    list_display = ("author", "quote", "private")
    actions = ["mark_private",
               "mark_public"]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'168'})},
        models.TextField: {'widget': Textarea(attrs={'rows':40, 'cols':120})},
        models.ManyToManyField: {'widget': SelectMultiple(attrs={'size':'15'})}
    }

    def mark_private(self, request, queryset):
        if type(queryset) == Quote:
            queryset.private = True
            queryset.save()
        else:
            for quote in queryset.all():
                quote.private = True
                quote.save()
    mark_private.short_description = "Mark selected as private"

    def mark_public(self, request, queryset):
        if type(queryset) == Quote:
            queryset.private = False
            queryset.save()
        else:
            for quote in queryset.all():
                quote.private = False
                quote.save()
    mark_public.short_description = "Mark selected as public"

admin.site.register(Quote, QuoteAdmin)


class CommentAdmin(admin.ModelAdmin):
    """ The admin model for a Comment.
    """
    list_display = ("name",
                    "subject",
                    "email",
                    "date")
    list_filter = ["name",
                   "date",
                   "private"]
    actions = ["mark_private",
               "mark_public",
               "delete_model"]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'168'})},
        models.TextField: {'widget': Textarea(attrs={'rows':40, 'cols':120})},
        models.ManyToManyField: {'widget': SelectMultiple(attrs={'size':'15'})}
    }

    def mark_private(self, request, queryset):
        if type(queryset) == Comment:
            queryset.private = True
            queryset.save()
        else:
            for comment in queryset.all():
                comment.private = True
                comment.save()
    mark_private.short_description = "Mark selected as private"

    def mark_public(self, request, queryset):
        if type(queryset) == Comment:
            queryset.private = False
            queryset.save()
        else:
            for comment in queryset.all():
                comment.private = False
                comment.save()
    mark_public.short_description = "Mark selected as public"

admin.site.register(Comment, CommentAdmin)


class PostAdmin(admin.ModelAdmin):
    """ The admin model for a Blog Post.
    """
    exclude = ('comments',)
    readonly_fields = ('view_count', 'content',)
    list_display = ("title",
                    "view_count",
                    "creation_date",
                    "private")
    list_filter = ["private",
                   "tags",
                   "creation_date"]
    actions = ["mark_private",
               "mark_public",]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'168'})},
        models.TextField: {'widget': Textarea(attrs={'rows':40, 'cols':120})},
        models.ManyToManyField: {'widget': SelectMultiple(attrs={'size':'15'})}
    }

    def mark_private(self, request, queryset):
        if type(queryset) == Post:
            queryset.private = True
            queryset.save()
        else:
            for post in queryset.all():
                post.private = True
                post.save()
    mark_private.short_description = "Mark selected as private"

    def mark_public(self, request, queryset):
        if type(queryset) == Post:
            queryset.private = False
            queryset.save()
        else:
            for post in queryset.all():
                post.private = False
                post.save()
    mark_public.short_description = "Mark selected as public"

admin.site.register(Post, PostAdmin)
