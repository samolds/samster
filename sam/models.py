from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from HTMLParser import HTMLParser
from django.conf import settings
from django.db import models
from PIL import Image
import markdown


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class Tag(models.Model):
    """Description of the Tag model
    """
    tag_help = "Hardcoded tags: 'top_about', 'top_contact', 'top_education', 'top_home', 'top_personal', 'top_professional', 'personal', 'thoughts', 'shower_thoughts', 'education', 'school', 'homework', 'professional', 'work', 'job', 'experience', 'project', 'banner_photo', 'art', 'drawing', 'photography'"

    tag = models.SlugField(max_length=50, unique=True, help_text=tag_help)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.tag

    def save(self, *args, **kwargs):
        if not Tag.objects.filter(tag=self.tag.lower()):
            self.tag = self.tag.lower()
            super(Tag, self).save(*args, **kwargs)
        else:
            raise ValidationError(u"The lowercase version of that tag already exists")

    class Meta:
        verbose_name = (u"Tag")
        verbose_name_plural = (u"Tags")


class Website(models.Model):
    """Description of the Website model
    """
    choices = (
        ('prsl', 'Personal'),
        ('mntn', 'Maintain'),
        ('dvlp', 'Develop'),
    )

    url = models.CharField(max_length=100, unique=True)
    display = models.CharField(max_length=50)
    note = models.CharField(max_length=50, blank=True, null=True)
    kind = models.CharField(max_length=4, choices=choices)
    private = models.BooleanField()

    def __unicode__(self):
        return "%s" % self.display

    def save(self, *args, **kwargs):
        self.url = self.url.lower()
        super(Website, self).save(*args, **kwargs)

    class Meta:
        verbose_name = (u"Website")
        verbose_name_plural = (u"Websites")


class Comment(models.Model):
    """Description of the Comment model
    """
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, blank=True, null=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    private = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        self.name = strip_tags(self.name)
        self.email = strip_tags(self.email)
        self.subject = strip_tags(self.subject)
        self.message = strip_tags(self.message)
        if self.email:
            sender = self.email
        else:
            sender = settings.DEFAULT_FROM_EMAIL
        try:
            email_message = "%s \n\n - %s (%s)" % (self.message, self.name, sender)
            send_mail(settings.SITENAME + " Comment - " + self.subject, email_message, sender, settings.CONTACT_EMAIL_RECIPIENT)
        except Exception as e:
            print e
        super(Comment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = (u"Comment")
        verbose_name_plural = (u"Comments")


class SiteImage(models.Model):
    """ Description of the SiteImage model
    """
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_markdown = models.TextField("Description", blank=True, null=True, help_text='<a href="http://daringfireball.net/projects/markdown/syntax">Markdown Help</a>')
    image = models.ImageField(upload_to="images", height_field="height", width_field="width")
    content_type = models.CharField(max_length=40)
    width = models.IntegerField()
    height = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, related_name='siteimage', blank=True, null=True)
    tags = models.ManyToManyField(Tag, max_length=50, related_name='siteimage', blank=True, null=True)
    private = models.BooleanField()
    view_count = models.IntegerField(default=0, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        content_types = {"JPEG": "image/jpeg", "GIF": "image/gif", "PNG": "image/png"}

        #if self.image.file.multiple_chunks():
            #img = Image.open(self.image.file.temporary_file_path())
        #else:
            #img = Image.open(self.image)

        #if not img.format in content_types:
            #raise ValidationError('Not an accepted image format')

        #self.content_type = content_types[img.format]

        if self.description_markdown:
            self.description = markdown.markdown(self.description_markdown)

        super(SiteImage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)

        super(SiteImage, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = (u"Image")
        verbose_name_plural = (u"Images")


class Quote(models.Model):
    """Description of the Quote model
    """
    name = models.CharField(max_length=50, blank=True, null=True)
    author = models.CharField(max_length=50)
    quote = models.TextField()
    tags = models.ManyToManyField(Tag, max_length=50, related_name='quote', blank=True, null=True)
    private = models.BooleanField()

    def __unicode__(self):
        if self.name:
            return "%s" % self.name
        else:
            return "%s" % self.author

    class Meta:
        verbose_name = (u"Quote")
        verbose_name_plural = (u"Quotes")
        ordering = ['-name']


class Post(models.Model):
    """Description of the Post model
    """
    title = models.CharField("title", max_length=100)
    content_markdown = models.TextField("Content", help_text='<a href="http://daringfireball.net/projects/markdown/syntax">Markdown Help</a>')
    content = models.TextField(blank=True, null=True)
    small_stub = models.TextField(blank=True, null=True)
    large_stub = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, max_length=50, related_name='post', blank=True, null=True)
    images = models.ManyToManyField(SiteImage, related_name='post', blank=True, null=True)
    embedded_link = models.CharField(max_length=500, blank=True, null=True)
    private = models.BooleanField()
    comments = models.ManyToManyField(Comment, related_name='post', blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.title

    def save(self):
        self.content = markdown.markdown(self.content_markdown)
        if self.small_stub == "":
            self.small_stub = markdown.markdown(self.content_markdown[:200].strip() + '...')
        if self.large_stub == "":
            self.large_stub = markdown.markdown(self.content_markdown[:750].strip() + '...')
        super(Post, self).save()

    class Meta:
        verbose_name = (u"Post")
        verbose_name_plural = (u"Posts")
