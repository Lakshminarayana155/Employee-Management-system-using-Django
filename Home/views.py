from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
#emp
from .models import Role, Employee, Department
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.html import escape

# Create your views here.
def home(request):
    return render(request,'index.htm')

def signup(request):
    

    if request.method=="POST":
        uname=request.POST['uname']
        fname=request.POST['fname']
        lname=request.POST['lname']
        uemail=request.POST['uemail']
        phone=request.POST['phone']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if User.objects.filter(username=uname):
            messages.error(request,"User name already exists! Please try some other username")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request,"Passwords didn't match")
            return redirect('signup')

        if not uname.isalnum():
            messages.error(request,"Username name should be alpha_numaric")
            return redirect('signup')
        myuser=User.objects.create_user(uname,uemail,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.phone=phone

        myuser.save()
        messages.success(request,"your account has been sucessfully created") 
        
        return redirect('signin')
    
    return render(request,'signup.htm')

def signin(request):
    
    if request.method=='POST':
        uname=request.POST['uname']
        pass1=request.POST['pass1']

        user= authenticate(username=uname,password=pass1)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,"index.htm",{"fname":fname})

        else:
            messages.error(request,"Invaid details")
            return redirect('home')
    
    return render(request,'signin.htm')
    



def signout(request):
    logout(request)
    messages.success(request,"Logged out sucessfully")
    return redirect('home')

def all_emply(request,page_n=1):
    # if request.method=='GET':
    #     rls=Role.objects.all()
    #     dpts=Department.objects.all()
    #     context = {
    #         'rls':rls,
    #         'dpts':dpts
    #      }
    #     return render(request,'all_emply.htm',context)

    rls=Role.objects.all()
    dpts=Department.objects.all()
    page_n=escape(page_n)
    emps=Employee.objects.all()
    ln=len(emps)
    p = Paginator(emps, 5)
    page_c=p.page(page_n)
    #code for r_nos
    emps=page_c.object_list
    
    r_n=(int(page_n)-1)*5+1
    r_nos=list(range(r_n,r_n+5))
    my_list=zip(r_nos,emps)
    context={
        "my_list":my_list,
        "ln" : ln,
        "pages":list(range(1,p.num_pages+1)),
        'rls':rls,
        'dpts':dpts
    }
    # print(context)
    return render(request,'all_emply.htm',context)


def add_emply(request):

    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone=request.POST['phone']
        salary=int(request.POST['salary'])
        dept=int(request.POST['dept'])
        bonus=int(request.POST['bonus'])
        role=request.POST['role']
        new_emp=Employee(first_name=first_name,last_name= last_name, phone=phone, salary= salary, bonus= bonus,dept_id= dept, role_id= role, hire_date= datetime.now())
        new_emp.save()
        context={
            "status":"Employee added sucessfully"
        }
        return render(request,'emply_add_status.htm',context)
    elif request.method=='GET':
        rls=Role.objects.all()
        dpts=Department.objects.all()
        context = {
            'rls':rls,
            'dpts':dpts
         }
        return render(request,'add_emply.htm',context)
    else:

        context={
            "status":"An exceptin occured! Employeed has not been added"
        }
        return render(request,'emply_add_status.htm',context)

def remove_emply(request,emp_id=0):
    if emp_id:
        try:
            emply_to_be_deleted=Employee.objects.get(id=emp_id)
            emply_to_be_deleted.delete()
            context={
                'status':"Employee remvoed sucessfully"
            }
            return render(request,"emply_add_status.htm",context)
        except:
            context={
                'status':"Please select an valid employee"
            }
            return render(request,"emply_add_status.htm",context)

    emps=Employee.objects.all()
    context = {
        'emps':emps
    }
    return render(request,'remove_emply.htm',context)

def filter_emply(request):
    if request.method =="POST":
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        sal = request.POST['salary']

        emps=Employee.objects.all()
        rls=Role.objects.all()
        dpts=Department.objects.all()

        if name:
            emps=emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps=emps.filter(dept__name__icontains = dept)
        if role:
            emps=emps.filter(role__name__icontains = role)
        if sal:
            emps=emps.filter( salary__gte =sal)
        
        
        r_ns=list(range(1,len(emps)+1))
        my_list=zip(r_ns,emps)
        context={
            "my_list":my_list,
            'rls':rls,
            'dpts':dpts

        }
        return render(request,'all_emply.htm',context)
    elif request.method == 'GET':
        depts=Department.objects.all()
        rls=Role.objects.all()
        context={
            'depts':depts,
            'rls':rls

        }
        return render(request,'filter_emply.htm',context)
    else:
        return HttpResponse('An Exception occured')




    return render(request,'filter_emply.htm')