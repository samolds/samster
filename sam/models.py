from django.db import models

class Posts(models.Model):
    """Description of the Posts model
    """
    name = models.CharField(max_length=100, blank=True)
    spottypes = models.ManyToManyField(SpotType, max_length=50, related_name='spots')
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True)
    height_from_sea_level = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    building_name = models.CharField(max_length=100, blank=True)
    floor = models.CharField(max_length=50, blank=True)
    room_number = models.CharField(max_length=25, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    display_access_restrictions = models.CharField(max_length=200, blank=True)
    organization = models.CharField(max_length=50, blank=True)
    manager = models.CharField(max_length=50, blank=True)
    etag = models.CharField(max_length=40)
    last_modified = models.DateTimeField(auto_now=True, auto_now_add=True)


class Images(models.Model):
    """ Description of the Images model
    """
    description = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="images", height_field="height", width_field="width")
    spot = models.ForeignKey(Spot)
    content_type = models.CharField(max_length=40)
    width = models.IntegerField()
    height = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    etag = models.CharField(max_length=40)
    upload_user = models.CharField(max_length=40)
    upload_application = models.CharField(max_length=100)

    def __unicode__(self):
        if self.description:
            return "%s" % self.description
        else:
            return "%s" % self.image.name

    def save(self, *args, **kwargs):
        self.etag = hashlib.sha1("{0} - {1}".format(random.random(), time.time())).hexdigest()

        content_types = {"JPEG": "image/jpeg", "GIF": "image/gif", "PNG": "image/png"}
        if self.image.file.multiple_chunks():
            img = Image.open(self.image.file.temporary_file_path())
        else:
            img = Image.open(self.image)

        if not img.format in content_types:
            raise ValidationError('Not an accepted image format')

        self.content_type = content_types[img.format]

        super(SpotImage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.etag = hashlib.sha1("{0} - {1}".format(random.random(), time.time())).hexdigest()
        self.image.delete(save=False)

        super(SpotImage, self).delete(*args, **kwargs)

    def rest_url(self):
        return "{0}/image/{1}".format(self.spot.rest_url(), self.pk)
