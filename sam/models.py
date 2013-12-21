from django.db import models
from PIL import Image


class Tag(models.Model):
    tag = models.SlugField(max_length=50)

    def __unicode__(self):
        return "%s" % self.tag


class SiteImage(models.Model):
    """ Description of the SiteImage model
    """
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    tags = models.ManyToManyField(Tag, max_length=50, related_name='image', blank=True, null=True)
    image = models.ImageField(upload_to="images", height_field="height", width_field="width")
    content_type = models.CharField(max_length=40)
    width = models.IntegerField()
    height = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, max_length=50, related_name='siteimage', blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        content_types = {"JPEG": "image/jpeg", "GIF": "image/gif", "PNG": "image/png"}
        if self.image.file.multiple_chunks():
            img = Image.open(self.image.file.temporary_file_path())
        else:
            img = Image.open(self.image)

        if not img.format in content_types:
            raise ValidationError('Not an accepted image format')

        self.content_type = content_types[img.format]

        super(SiteImage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)

        super(SiteImage, self).delete(*args, **kwargs)


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


class Post(models.Model):
    """Description of the Post model
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, max_length=50, related_name='post', blank=True, null=True)
    images = models.ManyToManyField(SiteImage, related_name='post', blank=True, null=True)
    embedded_link = models.CharField(max_length=500, blank=True, null=True)
    private = models.BooleanField()
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.title


class Art(models.Model):
    """Description of the Art model
    """
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, max_length=50, related_name='art', blank=True, null=True)
    image = models.ForeignKey(SiteImage)
    private = models.BooleanField()

    def __unicode__(self):
        return "%s" % self.title
