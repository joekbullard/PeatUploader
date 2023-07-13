from django.contrib.gis.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.core.exceptions import ValidationError
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


def get_upload_path(instance, filename):
    project = instance.project_id
    return f"images/{project}/{filename}"


class PeatContractor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    contact_email = models.EmailField(
        unique=True,
        blank=False,
        validators=[EmailValidator(message="Invalid email address")],
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    contractor = models.ForeignKey(PeatContractor, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class PeatProject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    project_id = models.CharField(max_length=5, unique=True, null=False, blank=False)
    contractor = models.ForeignKey(PeatContractor, on_delete=models.PROTECT)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class PeatPoint(models.Model):
    class MainCondition(models.TextChoices):
        DRAINED = "DN", "Drained"
        MODIFIED = "MD", "Modified"
        ACTIVELY_ERODING = "AE", "Actively eroding"
        NEAR_NATURAL = "NN", "Near natural"
        NOT_PEAT = "NP", "Not peat"
        FORESTED = "FR", "Forested"

    class SubCondition(models.TextChoices):
        HAGG_GULLY = "HG", "Hagg/gully"
        FLAT_BARE = "FB", "Flat/bare"
        ARTIFICIAL = "AR", "Artificial"
        GRASS = "GD", "Grass-dominated"
        HEATHER = "HD", "Heather-dominated"
        RUSH = "RD", "Rush-dominated"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.ForeignKey(PeatProject, on_delete=models.PROTECT)
    record_id = models.IntegerField()
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    record_date = models.DateField(null=False, blank=False)
    depth = models.IntegerField(
        null=True, validators=[MaxValueValidator(2000), MinValueValidator(0)]
    )
    main_condition = models.CharField(
        max_length=2, choices=MainCondition.choices, null=False, blank=False
    )
    sub_condition = models.CharField(max_length=2, choices=SubCondition.choices)
    notes = models.TextField()
    photo = ResizedImageField(
        size=[1980, 1080], upload_to=get_upload_path, blank=True, null=True
    )
    geom = models.PointField(srid=27700, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def clean_notes(self):
        if self.main_condition == "NP" and not self.notes:
            raise ValidationError("No explantion given for Not peatland condtion")

    class Meta:
        unique_together = ("project_id", "record_id")