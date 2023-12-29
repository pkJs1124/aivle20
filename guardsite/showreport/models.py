from django.db import models
from django.utils import timezone

class Checklist(models.Model):
    context = models.TextField()

    class Meta:
        db_table = 'checklist'

class ChecklistEntry(models.Model):
    create_at = models.DateField()
    context = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    truefalse = models.BooleanField()

    class Meta:
        db_table = 'report'