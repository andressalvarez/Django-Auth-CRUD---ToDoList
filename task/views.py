from django.shortcuts import render
#import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import login, logout # new import statement for login and authenticate
from django.db import IntegrityError # new import statement for IntegrityError
from django.contrib.auth import authenticate # new import statement for authenticate
from .form import TaskForm
from .models import Task
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required # new import statement for login_required
# Create your views here.
def index(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})

    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user=User.objects.create_user(username=request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(request, "/signup.html/", {"form": UserCreationForm, "error": "Username already exists"})
        return render(request, "/signup.html/", {"form": UserCreationForm, "error": "Passwords did not match"})
        
@login_required # this is a decorator that checks if the user is logged in
def tasks(request):#
    tasks =Task.objects.filter(user=request.user, datecompleted__isnull=True  )
    tasks_sorted = sorted(tasks, key=lambda task: task.important, reverse=True)# this is the user that is logged in se le pasa el usuario logueado
    return render(request, "tasks.html", {"tasks": tasks_sorted})

@login_required # this is a decorator that checks if the user is logged in
def completed_tasks(request):
    tasks =Task.objects.filter(user=request.user, datecompleted__isnull=False  ) # this is the user that is logged in se le pasa el usuario logueado
    return render(request, "tasks.html", {"tasks": tasks})

@login_required # this is a decorator that checks if the user is logged in
def cerrarsesion(request):
    logout(request)
    return redirect('index')


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html", {'form': AuthenticationForm})
    else:
        
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is None:
            return render(request, "login.html", {'form': AuthenticationForm, 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('tasks')

@login_required # this is a decorator that checks if the user is logged in
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm})
    else:
        try:
            form=TaskForm(request.POST)# this is the form that is being submitted recibe datos del formulario
            new_task=form.save(commit=False) # this is the form that is being saved guarda los datos netos del formulario
            new_task.user=request.user  # this is the user that is logged in guarda el usuario que esta logeado
            new_task.save() # this is the form that is being saved guarda los datos netos del formulario
            return redirect('tasks')
        except ValueError:
            return render(request, "create_task.html", {"form": TaskForm, "error": "Bad data passed in. Try again."})
        except:
            return render(request, "create_task.html", {"form": TaskForm, "error": "Something went wrong. Try again."})


@login_required # this is a decorator that checks if the user is logged in        
def task_detail(request, task_id):
    if request.method == "GET":
        task=get_object_or_404(Task, pk=task_id, user=request.user)
        form=TaskForm(instance=task)
        return render(request, "task_detail.html", {"task": task, "form": form})
    else:
        try:
            task=get_object_or_404(Task, pk=task_id, user=request.user)
            form=TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, "task_detail.html", {"task": task, "form": form, "error": "Bad info"})
        except:
            return render(request, "task_detail.html", {"task": task, "form": form, "error": "Something went wrong"})

@login_required # this is a decorator that checks if the user is logged in
def complete_task(request, task_id):
    task=get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted=timezone.now()
        task.save()
        return redirect('tasks')

@login_required # this is a decorator that checks if the user is logged in
def delete_task(request, task_id):
    task=get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


