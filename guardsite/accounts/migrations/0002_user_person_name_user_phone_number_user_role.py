# Generated by Django 4.2 on 2023-12-21 13:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="person_name",
            field=models.CharField(max_length=255, null=True, verbose_name="이름"),
        ),
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=models.CharField(max_length=15, null=True, verbose_name="전화번호"),
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[("admin", "관리자"), ("worker", "근로자")],
                default="worker",
                max_length=10,
            ),
        ),
    ]