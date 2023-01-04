from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Room, Message, Group
from .forms import SignUpForm

def home(request):
  rooms = Room.objects.all()
  groups = Group.objects.all()

  context = {
    "rooms": rooms,
    "groups": groups
  }
  return render(request, 'frontPage.html', context)

def signUpPage(request):
  form = SignUpForm()
  if request.method == 'POST':
    form = SignUpForm(request.POST)

    if form.is_valid():
      user = form.save()

      login(request, user)

      return redirect('Home')

  return render(request, 'auth/signupPage.html', {'form': form})

@login_required
def roomDetail(request, slug):
  room = Room.objects.get(slug=slug)
  messages = Message.objects.filter(room=room)
  rooms = Room.objects.all()
  groups = Group.objects.all()
  context = {
    "room": room,
    "messages": messages,
    "rooms": rooms,
    "groups": groups
  }
  return render(request, 'room/roomDetail.html', context)

@login_required
def groupDetail(request, slug):
  group = Group.objects.get(slug=slug)
  messages = Message.objects.filter(group=group)
  rooms = Room.objects.all()
  groups = Group.objects.all()
  context = {
    "group": group,
    "messages": messages,
    "rooms": rooms,
    "groups": groups
  }
  return render(request, 'group/groupDetail.html', context)