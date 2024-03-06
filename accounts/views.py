from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import ExtraUserData
from django.contrib import messages, auth
from .regex import usernameRegex, flNameRegex, emailRegex, passwordRegex, mkdPhoneRegex

# Not a django view 
def getContent(request, storage):
    for key in request.POST.keys():
        if request.POST[key] == "":
            messages.error(request, "All fields must be filled out")
            return False
        else:
            storage[key] = request.POST[key]
    return True

def register(request):
    if request.method != "POST":
        return render(request, "accounts/register.html")

    info = {}
    if not(getContent(request, info)):
        return redirect("register")
    
    if info["password"] != info["password2"]:
        messages.error(request, "Both entered password must be the same")
        return redirect("register")

    if User.objects.filter(username=info["username"]).exists():
        messages.error(request, "The entered username is already taken")
        return redirect("register")

    if not(usernameRegex.search(info["username"])):
        messages.error(request, "The entered username is invalid")
        return redirect("register")

    if not(flNameRegex.search(info["firstName"])):
        messages.error(request, "The entered first name is invalid")
        return redirect("register")

    if not(flNameRegex.search(info["lastName"])):
        messages.error(request, "The entered last name is invalid")
        return redirect("register")

    if User.objects.filter(email=info["email"]).exists():
        messages.error(request, "The entered email is already taken")
        return redirect("register")

    if not(emailRegex.search(info["email"])):
        messages.error(request, "The entered email is invalid")
        return redirect("register")

    if ExtraUserData.objects.filter(phoneNumber=info["phoneNumber"]).exists():
        messages.error(request, "The entered phone number is already taken")
        return redirect("register")

    if not(mkdPhoneRegex.search(info["phoneNumber"])):
        messages.error(request, "The entered phone number is invalid")
        return redirect("register")

    if ExtraUserData.objects.filter(adress=info["adress"]).exists():
        messages.error(request, "The entered adress is already taken")
        return redirect("register")

    if not(passwordRegex.search(info["password"])):
        messages.error(request, "The entered password is invalid")
        return redirect("register")
    
    user = User.objects.create_user(
        username = info["username"],
        first_name = info["firstName"],
        last_name = info["lastName"],
        email = info["email"],
        password = info["password"]
    )
    user.save()
    extraData = ExtraUserData.objects.create(
        user = user,
        adress = info["adress"],
        phoneNumber = info["phoneNumber"]
    )
    extraData.save()
    auth.login(request, user)
    messages.success(request, "You are registered and logged in")
    return redirect("index")

def login(request):
    if request.method != "POST":
        return render(request, "accounts/login.html")
    
    info = {}
    if not(getContent(request, info)):
        return redirect("login")

    user = auth.authenticate(
        username = info["username"],
        email = info["email"],
        password = info["password"]
    )

    if user is None:
        messages.error(request, "One of the entered values is invalid")
        return redirect("login")
    
    auth.login(request, user)
    messages.success(request, "You are logged in")
    return redirect("index")

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You are logged out")
    return redirect("index")