from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from todoapp.forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from todoapp.models import Task
from django.core.mail import send_mail
import datetime
from django.db.models import Q
import random
# Create your views here.
def home (request):
    return render(request,'todoapp/index.html')
def edit(request,rid):
    if request.method == "POST":
        upname=request.POST['name']
        updet=request.POST['tdetail']
        upc=request.POST['cat']
        ups=request.POST['status']
        updt=request.POST['duedate']

        t=Task.objects.filter(id=rid)
        t.update(name=upname,detail=updet,cat=upc,status=ups,enddate=updt)

        return redirect('/dashboard')
    else:

        t=Task.objects.filter(id=rid)
        content={}
        content['data']=t
        return render(request,'todoapp/edit.html',content)

def delete(request,rid):
    t=Task.objects.filter(id=rid)
    t.update(is_deleted=True)
    return redirect('/dashboard')

def dashboard (request):
    content={}
    # print("Authenticated user Id :",request.user.id)
    if request.method=="POST":
        #fetch data from form
        name=request.POST['name']
        det=request.POST['tdetail']
        c=request.POST['cat']
        s=request.POST['status']
        dt=request.POST['duedate']
        #create a new Task object
        u=User.objects.filter(id=request.user.id)
        t=Task.objects.create(name=name,detail=det,cat=c,status=s,enddate=dt,created_on=datetime.datetime.now(),uid=u[0])
        t.save()
        return redirect("/dashboard")
        
    else:
        q1=Q(uid=request.user.id)
        q2=Q(is_deleted= False)
        t=Task.objects.filter(q1 &q2)
        sendpendingemail(t)
        # print(t)
        content["data"]=t
        return render (request, 'todoapp/dashboard.html',content)


def user_register (request):
    content={}
    if request.method=="POST":
        un= request.POST['uname']
        p= request.POST['upass']
        cp= request.POST['ucpass']

        if un==''or p=='' or cp=='':
            content['errmsg']='Fields cannot be Empty'
        
        elif p!=cp:
            content['errmsg']="Password and Confirm Password didn't Matched"
        elif len(p)<8:
            content['errmsg']='Password must be atleast 8 charaters'
        else:
            try:
                u=User.objects.create(username=un,email=un)
                u.set_password(p)
                u.save()
                content['success']="User register Successfully!! Please Login"

            except Exception:
                content['errmsg']='User with same Already Existed'
        return render (request,'accounts/register.html',content)
    else:

        return render (request, 'accounts/register.html')
    

def user_login(request):
    content={}
    if request.method=="POST":
        un= request.POST['uname']
        p= request.POST['upass']
        u=authenticate(username=un,password=p)
        # print(u)
        if u is not None:
            login(request,u)
            return redirect('/dashboard')
        else:
            content['errmsg']='Invalid Username and Password'
            return render(request,'accounts/login.html',content)
            
    else:
        return render(request,'accounts/login.html')


def user_logout (request):
    logout(request) #destroy session.delete all data from session 
    return redirect('/login')

def catfilter(request,cv):
    q1=Q(uid = request.user.id)
    q2=Q(is_deleted=False)
    q3=Q(cat=cv)

    t=Task.objects.filter(q1 & q2 & q3)
    content={}
    content['data']=t
    return render(request,'todoapp/dashboard.html',content)


def statfilter(request,cv):
    q1=Q(uid = request.user.id)
    q2=Q(status=cv)

    t=Task.objects.filter(q1 & q2)
    content={}
    content['data']=t
    return render(request,'todoapp/dashboard.html',content)


def datefilter(request):
    frm=request.GET['from']
    to=request.GET['to']

    q1=Q(uid=request.user.id)
    q2=Q(is_deleted=False)
    q3=Q(enddate__gte=frm)
    q4=Q(enddate__lte=to)
    t=Task.objects.order_by('enddate').filter(q3&q4).filter(q1 & q2)
    content={}
    content['data']=t
    # print(t)

    return render(request,'todoapp/dashboard.html',content)

def datesort(request,ds):
    q2=Q(is_deleted=False)
    q1=Q(uid = request.user.id)
    if  ds=='0' :
        col='-enddate'
    else: 
        col='enddate'
    
    t=Task.objects.order_by(col).filter(q1 & q2)
    # print(t)
    content={}
    content['data']=t
    return render(request,'todoapp/dashboard.html',content)


def sendpendingemail(t):

    # print("In Pending email: ")
    # print(t)
    for x in t:
        if x.status == 0:
            d=x.enddate.day
            currentdate =datetime.datetime.now().day
            # print(currentdate)
            diff= d-currentdate
            # print(diff)
            if diff==1:
                rec=x.uid.email
                print(rec)
                subject="REMINDER"
                msg=x.name + "Task is Due for 1 day"
                sender='sabagwan07@gmail.com'
                send_mail(
                subject,
                msg,
                sender,
                [rec],
                fail_sl
                )

    