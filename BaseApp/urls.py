from django.contrib import auth
from django.urls import path
from django.urls.conf import include
from . import views
from django.contrib.auth import views as authviews

urlpatterns = [
    path('signup/',views.SignUpView, name='signup'),
    path('',views.RedirectHomeView, name = 'redirecthome'),
    path('login/',views.LoginView,name = 'login'),
    path('home/',views.HomeView, name = 'home'),
    path('dashboard/',views.DashBoardView, name = 'dashboard'),
    path('logout/',views.LogoutView,name = 'logout'),
    path('password/reset/',views.PasswordResetView, name = 'password_reset'),
    path('password/reset/done/',authviews.PasswordResetDoneView.as_view(),name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/',authviews.PasswordResetConfirmView.as_view(),name = 'password_reset_confirm'),
    path('reset/done/',authviews.PasswordResetCompleteView.as_view(), name = 'password_reset_complete'),
    path('accounts/login/',views.RedirectView,name = 'redirectlogin'),
    path('dashboard/',views.DashBoardView, name = 'dashboard'),
    path('quiz/current/',views.QuizCurrentView, name = 'quizcurrent'),
    path('quiz/past/',views.QuizPastView,name = 'quizpast'),
    path('quiz/future',views.QuizFutureView, name = 'quizfuture'),
    path('dashboard/<int:id>',views.QuizView, name = 'quiz'),
    path('dashboard/<int:id>/<int:no>',views.QuestionView, name = 'question'),
    path('submit/',views.SubmitView,name = 'submit'),
    path('evalquiz/<int:id>',views.EvaluatedQuizView,name = 'evalquiz'),
    path('submission/',views.SubmissionView, name = "submission"),
    path('accounts/',include('allauth.urls')),
    path('googlelogin/',views.LoginGoogleView, name = 'logingoogle'),
    path('base/',views.base, name = 'base'),

]