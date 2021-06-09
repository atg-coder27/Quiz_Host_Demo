from django.contrib.auth import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.contrib.auth.forms import AuthenticationForm
from django.forms.models import BaseModelFormSet
from .models import ChoiceMCQ
from django.forms import modelformset_factory




class SignUpForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','first_name','last_name','email']
    
class AuthForm(AuthenticationForm):
    class Meta:
        model = User 
        fields = '__all__'

class ChoiceMCQForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ChoiceMCQForm,self).__init__(*args,**kwargs)
        self.fields['title'].required = False 
        self.fields['select'].required = False
    class Meta:
        model = ChoiceMCQ
        fields = ['title','select']

ChoiceMCQFormset = modelformset_factory(ChoiceMCQ, form = ChoiceMCQForm , extra=0)

    


    
    



