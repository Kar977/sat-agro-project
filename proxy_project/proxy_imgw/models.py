from django.core.validators import MaxValueValidator
from django.db import models


class Warning(models.Model):
    """
    Store IMGW meteorological warnings.
    We store key fields and the raw JSON payload.
    """

    teryt = models.CharField(max_length=4, db_index=True)
    imgw_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    title = models.CharField(max_length=255)
    level = models.CharField(max_length=50, blank=True, null=True)
    possibility = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    published = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    comment = models.CharField(max_length=255)
    office = models.CharField(max_length=255)
    areas = models.JSONField(blank=True, null=True)
    raw = models.JSONField()
    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start"]

    def __str__(self):
        return f"{self.title} ({self.level})"
