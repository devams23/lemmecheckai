from django.db import models

class PDFUpload(models.Model):
    pdf_file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    pdf_upload = models.ForeignKey(PDFUpload, on_delete=models.CASCADE)
    question_text = models.TextField()

class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100, blank=True, null=True)
    is_correct = models.BooleanField(default=False)
