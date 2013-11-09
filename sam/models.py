from django.db import models


class Image(models.Model):
    """ Description of the Image model
    """
    description = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="images", height_field="height", width_field="width")
    content_type = models.CharField(max_length=40)
    width = models.IntegerField()
    height = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if self.description:
            return "%s" % self.description
        else:
            return "%s" % self.image.name

    def save(self, *args, **kwargs):
        content_types = {"JPEG": "image/jpeg", "GIF": "image/gif", "PNG": "image/png"}
        if self.image.file.multiple_chunks():
            img = Image.open(self.image.file.temporary_file_path())
        else:
            img = Image.open(self.image)

        if not img.format in content_types:
            raise ValidationError('Not an accepted image format')

        self.content_type = content_types[img.format]

        super(Image, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)

        super(Image, self).delete(*args, **kwargs)


class Quote(models.Model):
    """Description of the Quote model
    """
    author = models.CharField(max_length=50, blank=True)
    quote = models.TextField()


class Post(models.Model):
    """Description of the Post model
    """
    title = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    #image = models.ImageField(upload_to="images", height_field="height", width_field="width")
    image = models.ForeignKey(Image)


class Art(models.Model):
    """Description of the Art model
    """
    title = models.CharField(max_length=100, blank=True)
    tags = models.CharField(max_length=100, blank=True)
    #image = models.ImageField(upload_to="images", height_field="height", width_field="width")
    image = models.ForeignKey(Image)
