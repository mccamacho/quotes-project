from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "index.html")


def register(request):
    print(request.POST)
    errors = User.objects.registrationvalidator(request.POST)
    print(errors)
    print(len(errors))
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        password=request.POST['password']
        print(password)
        hashedpassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(hashedpassword)
        user = User.objects.create(name = request.POST["name"], 
        email = request.POST["email"], 
        password = hashedpassword.decode())
        print(user)
        request.session['id'] = user.id
    return redirect("/quotes")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    request.session['id']= User.objects.filter(email= request.POST['email'])[0].id
    return redirect("/quotes")

def dashboard(request):
    if 'id' not in request.session:

        return redirect('/')
    user=User.objects.get(id=request.session['id'])
    context={
        'loggedinUser':User.objects.get(id=request.session['id']),
        'favorites':Quote.objects.filter(favorites=user),
        'allquotes':Quote.objects.exclude(favorites=user),
        'allusers':User.objects.all()
    }
    return render (request, "dashboard.html", context)

def addquote(request):
    print(request.POST)
    user = User.objects.get(id=request.session['id'])
    errors= Quote.objects.quote_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/quotes")
    else:
        user = Quote.objects.create(message= request.POST['message'], quote_owner= request.POST['owner'], poster=user)
        print(user)
        return redirect("/quotes")

def showuser(request, number):
    if 'id' not in request.session:
        
        return redirect('/')
    else:
        user = User.objects.get(id=number)
        context={
            'user': User.objects.get(id=number),
            'quotes': Quote.objects.filter(poster=user)
        }
        return render(request, "showuser.html",context)

def logout(request):
    request.session.clear()
    return redirect("/")

def editquote(request, number):
    if 'id' not in request.session:
        
        return redirect('/')
    else:
        context={
            'quote': Quote.objects.get(id=number)
        }
        return render(request, "editquote.html", context)

def update(request,number):
    user=User.objects.get(id=request.session['id'])
    errors= Quote.objects.quote_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/quotes/"+str(number))
    else:
        update=Quote.objects.get(id=number)
        update.message= request.POST['message']
        update.quote_owner=request.POST['owner']
        update.poster= user
        update.save()
        return redirect("/quotes")

def addtofavorite(request, number):
    user= User.objects.get(id=request.session['id'])
    quote=Quote.objects.get(id=number)
    quote.favorites.add(user)
    return redirect("/quotes")
def removefromfavorite(request, number):
    user= User.objects.get(id=request.session['id'])
    quote=Quote.objects.get(id=number)
    quote.favorites.remove(user)
    return redirect("/quotes")
    
     
def delete(request, number):
    quote= Quote.objects.get(id=number)
    quote.delete()
    return redirect("/quotes")

# def showallBookReviews(request):
#     if 'id' not in request.session:
#          return redirect("/")
#     else:
#         context={
#             "loggedinUser": User.objects.get(id= request.session['id']),
#             "allreviews": Review.objects.all()
#         }
#         return render(request, "books.html", context)