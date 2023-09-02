from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo
from django.utils import timezone


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],
                                                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Пользователь с таким именем уже существует!'})
        else:
            return render(request, 'todo/signupuser.html',
                          {'form': UserCreationForm(),
                           'error': 'Пароли не совпали!'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'Неверные данные для входа!'})
        else:
            login(request, user)
            return redirect('current')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def currenttodos(request):
    todos = Todo.objects.filter(user=request.user)
                                # date_completed__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})

def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST, request.FILES)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current')
        except ValueError:
            return render(request, 'todo/createtodo.html',
                          {'form': TodoForm(),
                           'error': 'Переданы неверные данные!'})

def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    form = TodoForm(instance=todo)
    if request.method == 'GET':
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current')
        except ValueError:
            return render(request, 'todo/viewtodo.html',
                          {'form': form,
                           'error': 'Неверные данные!'})


def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('current')

def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current')

