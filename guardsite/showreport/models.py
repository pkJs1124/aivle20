from django.db import models

class ChecklistEntry(models.Model):
    create_at = models.DateField()
    # list_num = models.IntegerField()
    truefalse = models.BooleanField()
 
    class Meta:
        db_table = 'report'