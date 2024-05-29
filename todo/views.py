from django.shortcuts import render, redirect
from  django.http import HttpResponse, HttpResponseNotAllowed

# Create your views here.
from .forms import  CreateUserForm, LoginForm, CreateTaskForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Task, Profile
from django.contrib import messages


def home(request):

    
    return render(request,"home.html")


def register(request):
    form = CreateUserForm()


    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():
            current_user = form.save(commit=False)
            form.save()

            profile = Profile.objects.create(user=current_user)
            messages.success(request, "Registered Successfully")
            return redirect("login")
        else:
            messages.error(request, "Error While Registering the user, please try again")
            return redirect("register")
        
    return render(request, 'register.html', {"form":form})

def login(request):
    
    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    
    return render(request, 'login.html', {"form": form})

def logout(request):
    auth.logout(request)

    return redirect("")
    
@login_required(login_url='/login')
def dashboard(request):
    user = request.user
    current_user = request.user.id
    profile = Profile.objects.get(user=user)
    task = Task.objects.all().filter(user=current_user)
    return render(request,"user/dashboard.html", {"user": user, 'task': task, "profile": profile})


@login_required(login_url='/login')
def createTask(request):

    form = CreateTaskForm()

    if request.method == 'POST':

        form = CreateTaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user

            task.save()

            return redirect('view-tasks')
        
    return render(request,"user/create-task.html", {'form':form})

@login_required(login_url='/login')
def viewTasks(request):

    current_user = request.user.id

    task = Task.objects.all().filter(user=current_user)

    return render(request, 'user/view-tasks.html', {"task":task})    

@login_required(login_url='/login')
def updateTask(request, pk):

    task = Task.objects.get(id=pk)

    form = CreateTaskForm(instance=task)

    if request.method == 'POST':

        form = CreateTaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()

            return redirect('view-tasks')


    return render(request, 'user/update-task.html', {"form":form})    

@login_required(login_url='/login')
def deleteTask(request, pk):

    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()

        return redirect('view-tasks')
     
    return render(request, 'user/delete-task.html',{"task": task})    
