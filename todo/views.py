from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login , logout
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import authenticate 
from .foms import ToDoForm
from .models import ToDo
from django.shortcuts import get_object_or_404
from django.utils import timezone





def home(request):
    return render(request, 'todo/home.html')



def singupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/singupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
              return render(request, 'todo/singupuser.html', {'form':UserCreationForm(), 'error': 'Пользователь с таким именем уже есть'})  
        else:
            print('Ощибка')
            return render(request, 'todo/singupuser.html', {'form':UserCreationForm(), 'error': 'Пароли не совпадают'})
        
def currenttodos(request):
    # ! Не подходит
    # todos = ToDo.objects.all()
    todos = ToDo.objects.filter(user=request.user, datacompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    

def loginuser(request):
    if request.method == 'GET':
         return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password1'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Такого пользователя нет!'})
        else:
            login(request, user)
            return redirect('currenttodos')
        

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/currenttodo.html', {'form':ToDoForm()})
    else:
        form = ToDoForm(request.POST)
        newtodo = form.save(commit=False)
        newtodo.user = request.user
        newtodo.save()
        return redirect('currenttodos')


def viewtodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = ToDoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else: 
        form = ToDoForm(request.POST, instance=todo)
        form.save()
        return redirect('currenttodos')


def completetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datacompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')
    

def deletetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')



def completedtodo(request):
    todos = ToDo.objects.filter(user=request.user, datacompleted__isnull=False).order_by('-datacompleted')
    return render(request, 'todo/completedtodo.html', {'todos': todos})