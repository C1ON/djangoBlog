import time

from django.shortcuts import render, redirect
from .forms import RegisterForm, loginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages


# Create your views here.


def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username=username)
        newUser.set_password(password)

        newUser.save()
        login(request, newUser)  # Kayıt olan kullanıcının otomatik girişini sağlar.

        messages.info(request, "Başarıyla kayıt olundu.")

        return redirect("index")
    else:
        context = {
            "form": form
        }
        return render(request, "register.html", context)


"""  if request.method == "POST":
      form = RegisterForm(request.POST)
      if form.is_valid():
          username = form.cleaned_data.get("username")
          password = form.cleaned_data.get("password")

          newUser = User(username = username)
          newUser.set_password(password)

          newUser.save()
          login(request,newUser) # Kayıt olan kullanıcının otomatik girişini sağlar.

          return redirect("index")

      else:
          context = {
              "form": form
          }
          return render(request, "register.html", context)

  else:
      form = RegisterForm()
      context={
          "form":form
      }
      return render(request,"register.html",context)    """


def loginUser(request):
    form = loginForm(request.POST or None)

    context = {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Kullanıcı adı veya parola hatalı!")

            return render(request, "login.html", context)

        else:
            login(request, user)

            return redirect("index")
    else:
        return render(request, "login.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla çıkış yapıldı.")

    return redirect("index")