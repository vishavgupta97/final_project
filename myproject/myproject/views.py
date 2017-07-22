# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from datetime import datetime
from  myapp.forms import SignUpForm,LoginForm
from myapp.models import UserModel
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.
def signup_view(request) :
    #Business Logic starts here

    if request.method=='GET' :  #IF GET REQUEST IS RECIEVED THEN DISPLAY THE SIGNUP FORM
        today=datetime.now()
        form = SignUpForm()
        #template_name='signup.html'
        return render(request,'signup.html',{'form':form})

    elif request.method=='POST' :
        form = SignUpForm(request.POST)
        if form.is_valid() : #Checks While Valid Entries Is Performed Or Not
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            name=form.cleaned_data['name']
            password=form.cleaned_data['password']
            #here above cleaned_data is used so that data could be extracted in safe manner,checks SQL injections

            #following code inserts data into database
            new_user=UserModel(name=name,password=make_password(password),username=username,email=email)
            new_user.save()   #finally saves the data in database
            #template_name='success.html'

        return render(request,'success.html',{'form': form})

def login_view(request) :
    if request.method == 'GET' :#display form
        template='login.html'    #it will redirect to login page
        form = LoginForm()       #object

    elif request.method =='POST' :
        form = LoginForm(request.POST)
        if form.is_valid() :             #checks whether entriesd in form is valid or not
            username=form.cleaned_data['username']      #extracting username and password in secure way
            password=form.cleaned_data['password']      #which was entered by user in login form
            #check user exists in database or not
            user=UserModel.objects.filter(username=username).first()    #reads data from database
            #Above SELECT * from user model where username=username
            #This is SQL Querie for above statement

            if user :  #checks whether user exist in database or not
                #comparison of password here
                #comparison sof password here
                if check_password(password,user.password) :
                    #login successful here
                    template = 'login_success.html'
                else:
                    #password is incorrect
                    template = 'login_fail.html'
            else :
                template ='login_fail.html'
    return render(request,template,{'form':form})