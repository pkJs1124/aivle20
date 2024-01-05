from django.db import models
from accounts.models import User

class Checklist(models.Model):
    context = models.TextField()

    class Meta:
        db_table = 'checklist'

class ChecklistEntry(models.Model):
    create_at = models.DateField()
    context = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    truefalse = models.BooleanField()
    # user = models.ForeignKey(User.person_name, on_delete=models.CASCADE)

    class Meta:
        db_table = 'report'