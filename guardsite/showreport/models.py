from django.db import models
from accounts.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

class Checklist(models.Model):
    context = models.TextField()

    class Meta:
        db_table = 'checklist'
        
    # def save(self, *args, **kwargs):
    #     # 같은 날짜에 대한 데이터 개수 확인
    #     existing_count = Checklist.objects.filter(date=self.date).count()

    #     # 데이터 개수가 12개 이하인 경우에만 저장
    #     if existing_count < 12:
    #         super().save(*args, **kwargs)
    #     else:
    #         raise ValidationError("Cannot create more than 12 entries for the same date.")

class ChecklistEntry(models.Model):
    create_at = models.DateField()
    context = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    truefalse = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'report'