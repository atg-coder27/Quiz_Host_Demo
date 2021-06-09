from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Quiz(models.Model):
    category = models.CharField(max_length=40)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null = False)
    choices = (
        ('Completed','Completed'),
        ('Ongoing','Ongoing'),
        ('Future','Future'))
    status = models.CharField(max_length=20,choices=choices)

    def __str__(self) -> str:
        return self.category
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete= models.CASCADE)
    title = models.TextField()
    choices = (('MCQ','MCQ'),('Subjective','Subjective'))
    type = models.CharField(max_length=20, choices = choices)
    total = models.IntegerField(default=1)
    current_no = models.IntegerField(default=None,null = True)
    def __str__(self) -> str:
        return self.title


class ChoiceMCQ(models.Model):
    question = models.ForeignKey(Question,on_delete= models.CASCADE)
    title = models.CharField(max_length=100)
    select = models.BooleanField(default=False)
    correct = models.BooleanField(default=False)

class ChoiceSubjective(models.Model):
    question = models.ForeignKey(Question,on_delete= models.CASCADE)
    title = models.CharField(max_length= 300)
    file = models.FileField(upload_to='documents/')
    upload_time = models.DateTimeField(auto_now_add= True)

class CompletedQuiz(models.Model):
    category = models.CharField(max_length=40,editable=False)
    start_time = models.DateTimeField(null=False,editable=False)
    end_time = models.DateTimeField(null = False,editable=False)
    session = models.BooleanField(default= False,editable=False)
    completed = models.BooleanField(default=False,editable=False)

class CompletedQuestion(models.Model):
    quiz = models.ForeignKey(CompletedQuiz,on_delete= models.CASCADE,editable=False)
    title = models.TextField(editable = False)
    choices = (('MCQ','MCQ'),('Subjective','Subjective'))
    type = models.CharField(max_length=20, choices = choices,editable=False)
    total = models.IntegerField(editable=False)
    current_no = models.IntegerField(default=None,editable=False)

class CompletedChoiceMCQ(models.Model):
    question = models.ForeignKey(CompletedQuestion,on_delete= models.CASCADE,editable=False)
    title = models.CharField(max_length=100,editable=False)
    select = models.BooleanField(default=False,editable=False)
    correct = models.BooleanField(default=False,editable=False)

class CompletedChoiceSubjective(models.Model):
    question = models.ForeignKey(Question,on_delete= models.CASCADE)
    title = models.CharField(max_length= 300)
    file = models.FileField(upload_to='documents/')
    upload_time = models.DateTimeField(auto_now_add= True)







