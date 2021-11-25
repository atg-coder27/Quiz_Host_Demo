from django.contrib import admin
from .models import Question,Quiz,ChoiceMCQ,ChoiceSubjective
from .models import CompletedQuiz,CompletedQuestion,CompletedChoiceMCQ,CompletedChoiceSubjective

# Register your models here.

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('category','start_time','end_time','status')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz','title','type','total')

@admin.register(ChoiceMCQ)
class ChoiceMCQAdmin(admin.ModelAdmin):
    list_display = ('question','title','select','correct')

@admin.register(ChoiceSubjective)
class ChoceSubjectiveAdmin(admin.ModelAdmin):
    list_display = ('question','title','file','upload_time')

@admin.register(CompletedQuiz)
class CompletedQuizAdmin(admin.ModelAdmin):
    list_display = ('category','start_time','end_time')

@admin.register(CompletedQuestion)
class CompletedQuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz','title','type','total')

@admin.register(CompletedChoiceMCQ)
class CompletedChoiceMCQAdmin(admin.ModelAdmin):
    list_display = ('question','title','select','correct')

# @admin.register(CompletedChoiceSubjective)
# class CompletedChoceSubjectiveAdmin(admin.ModelAdmin):
#     list_display = ('question','title','file','upload_time')



