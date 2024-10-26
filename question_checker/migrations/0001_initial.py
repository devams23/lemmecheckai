# Generated by Django 5.1.2 on 2024-10-25 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PDFUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('pdf_upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_checker.pdfupload')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_answer', models.CharField(max_length=100)),
                ('correct_answer', models.CharField(blank=True, max_length=100, null=True)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_checker.question')),
            ],
        ),
    ]
