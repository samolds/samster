from django.shortcuts import render_to_response
from django.template import RequestContext
from sam.models import Tag, Post, SiteImage
from django.db.models import Q


def education(request):
    tag = Tag.objects.filter(tag="top_education")
    post = None
    images = []
    if tag:
        posts = list(Post.objects.filter(tags=tag))
        if posts:
            post = posts[-1]
            for image in post.images.values():
                images.append(SiteImage.objects.get(image=image['image']))
            images.reverse()

    public = Q(private=False)
    education = Q(tags__tag="education")
    school = Q(tags__tag="school")
    homework = Q(tags__tag="homework")

    posts = Post.objects.filter(education | school | homework)
    posts = list(set(posts.filter(public)))
    if len(posts) > 2:
        posts = posts[len(posts) - 2:]
    posts.reverse()
    full_post_stub = False

    return render_to_response('education.html', {
        "post": post,
        "images": images,
        "posts": posts,
        "full_post_stub": full_post_stub
    }, context_instance=RequestContext(request))
