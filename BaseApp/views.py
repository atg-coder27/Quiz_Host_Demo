from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .forms import ChoiceMCQForm, SignUpForm,AuthForm,ChoiceMCQFormset
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse,HttpResponseRedirect
from .models import Quiz,Question,ChoiceMCQ,ChoiceSubjective,CompletedChoiceMCQ,CompletedChoiceSubjective,CompletedQuestion,CompletedQuiz
from datetime import datetime
from django.forms import fields, modelformset_factory
from .save import SaveToModel
import json
from rest_framework.response import Response
from .serializers import QuestionSerializer

# Create your views here.


def HomeView(request):
    return render(request,'BaseApp/home.html')

def RedirectHomeView(request):
    return HttpResponseRedirect('/home')

def SignUpView(request):
    if request.method ==  'POST':
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/home')
    else:
        fm = SignUpForm()
    return render(request,'BaseApp/signup.html',{'form':fm})

def LoginView(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthForm(request=request, data = request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname,password= upass)
                if user != None:
                    login(request,user)
                    return HttpResponseRedirect('/dashboard')
        else:
            fm = AuthForm()
        
        return render(request,'BaseApp/login.html',{'form':fm})
        
    else:
        return HttpResponseRedirect('/dashboard')

def LoginGoogleView(request):
    return render(request,'BaseApp/google.html')

def LogoutView(request):
    logout(request)
    return HttpResponseRedirect('/home')

def PasswordResetView(request):
    if request.method == 'POST':
        form = PasswordResetForm(data = request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            queryset = User.objects.filter(email = email)
            if len(queryset) != 0:
                for user in queryset:
                    subject = "Password Change"
                    email_template = 'password/password_reset_email.txt'
                    c = {
                        "email" : user.email,
                        "domain" : "127.0.0.1:8000",
                        'site_name': 'Website',
					    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
					    "user": user,
					    'token': default_token_generator.make_token(user),
					    'protocol': 'http',
                    }
                    email = render_to_string(email_template,c)
                    try:
                        send_mail(subject,email,'admin@example.com',[user.email],fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid Header Found')
                    return HttpResponseRedirect('/password/reset/done')
        return HttpResponseRedirect('/home')
    else:
        form = PasswordResetForm()
        return render(request,'password/password_reset.html',{'form':form})

def RedirectView(request):
    return HttpResponseRedirect('/login')


def DashBoardView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    ongoing_quiz = Quiz.objects.filter(status = 'Ongoing')
    future_quiz = Quiz.objects.filter(status = 'Future')
    past_quiz = CompletedQuiz.objects.all()
    return render(request,'BaseApp/dashboard.html',{
        'ongoing':ongoing_quiz,'future':future_quiz, 'completed':past_quiz}
    )

def QuizCurrentView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    ongoing_quiz = Quiz.objects.filter(status = 'Ongoing')
    return render(request,'BaseApp/quiz_current.html',{'ongoing':ongoing_quiz})

def QuizPastView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    past_quiz = CompletedQuiz.objects.all()
    return render(request,'BaseApp/quiz_past.html',{'completed':past_quiz})

def QuizFutureView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    future_quiz = Quiz.objects.filter(status = 'Future')
    return render(request,'BaseApp/quiz_future.html',{'future':future_quiz})

def QuizView(request,id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    quiz = Quiz.objects.get(id = id)
    if quiz.status == "Completed":
        return HttpResponseRedirect("/submission")
    questions = Question.objects.filter(quiz = quiz)
    if len(questions) == 0:
        return HttpResponse("No Questions")
    return render(request,'BaseApp/quiz.html',{'quiz':quiz})


def QuestionView(request,id,no):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    quiz = Quiz.objects.get(id = id)
    if quiz.status == "Completed":
        SaveToModel(id)
        return HttpResponseRedirect('/submission')


    if request.method == "GET":
        question = Question.objects.get(quiz = quiz, current_no = no)
        queryset = ChoiceMCQ.objects.filter(question = question)
        formset = ChoiceMCQFormset(queryset= queryset)
        last = len(Question.objects.filter(quiz = quiz))
        start = 1
        question = question.__dict__
        value = QuestionSerializer(question)
        result = Response(value.data)
        print(result)
        return render(request,'BaseApp/question.html',{"question":question,
        'form' : formset, "last" : last , "start" : start , "current" : no })
    
    if request.method == "POST" :
        question = Question.objects.get(quiz = quiz, current_no = no)
        queryset = ChoiceMCQ.objects.filter(question = question)
        print(queryset)
        formset = ChoiceMCQFormset(data = request.POST, queryset= queryset)
        if formset.is_valid():
            instances = formset.save(commit=False)
            print(instances)
            for instance in instances:
                instance.save()

        if "next" in request.POST:
            url = "/dashboard/{}/{}".format(id,no+1)
            return HttpResponseRedirect(url)
        elif "previous" in request.POST:
            url = "/dashboard/{}/{}".format(id,no-1)
            return HttpResponseRedirect(url)
        else:
            request.session['previous'] = (id,no)
            return HttpResponseRedirect('/submit')

def SubmitView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    if request.method == "GET":
        return render(request,"BaseApp/submit.html")
    if request.method == "POST":
        id,no = request.session['previous']
        prev_url = "/dashboard/{}/{}".format(id,no)
        if "Yes" in request.POST:
            SaveToModel(id)
            return HttpResponseRedirect('/submission')  
        else:
            return HttpResponseRedirect(prev_url)

def SubmissionView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    return render(request,"BaseApp/submission.html")

def EvaluatedQuizView(request,id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home')
    quiz = CompletedQuiz.objects.get(id = id)
    questions = CompletedQuestion.objects.filter(quiz = quiz)
    data_question = []
    for question in questions:
        ques_dic = question.__dict__
        choices = list(CompletedChoiceMCQ.objects.filter(question = question))
        choices = [j.__dict__ for j in choices]
        ques_dic['choices'] = choices
        data_question.append(ques_dic)
    data = quiz.__dict__
    data['questions'] = data_question

    return render(request,"BaseApp/evalquiz.html",{'data':data})


def base(request):
    return render(request,'BaseApp/base.html')       

    
        
    


    
    
# {% for fm in form %}
#     {{fm.label_tag}} {{fm}} {{fm.errors|striptags}} <br> <br>
# {% endfor %}
        





