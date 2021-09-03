from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User
import bcrypt
from datetime import datetime
# Create your views here.


def fusion(request):

    if "usuario" in request.session:
        messages.info(request,"Ya estas logueado!!")
        return redirect("/")

    return render(request, "account/extend.html")

def logout(request): 
    if "usuario" in request.session:
        del request.session["usuario"]
    return redirect("/account")

def login(request):
    # if request.method == "GET":
    #     if "usuario" in request.session:
    #         messages.info(request,"Ya estas logueado!!")
    #         return redirect("/index")
    #     return render(request,"app/login.html")


    if request.method == "POST":
        usuario = User.objects.filter(email = request.POST["email"])
        if usuario:
            logged_user = usuario[0]
        else:
            messages.warning(request,"El email no se encuentra registrado!")
            return redirect("/account")

        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):

            request.session["usuario"] = {
                "id" : logged_user.id,
                "nombre" : f"{logged_user.nombre}",
                "alias" : logged_user.alias,
                "email" : logged_user.email,
                "fecha_nacimiento" : str(logged_user.fecha_nacimiento)
            }
            messages.success(request,"Logueado correctamente! :D")
            return redirect("/")
        else:
            messages.error(request,"Contraseña incorrecta!")
        return redirect("/account")


def register(request):
    # if request.method == "GET":
    #     return render(request,"app/register.html")


    if request.method == "POST":
        print(request.POST)
        print(request.POST["fecha_nacimiento"])
        errors = User.objects.validator(request.POST)
        print(errors)
        if len(errors) > 0 :
            
            for key, value in errors.items():

                messages.error(request,value)

            return redirect("/account")   

        else:
            new_user = User.objects.create(
                nombre = request.POST["nombre"],
                alias = request.POST["alias"],
                email = request.POST["email"],
                fecha_nacimiento = request.POST["fecha_nacimiento"],
                password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
            )
            print("SE HA CREADO LA CUENTA")
            messages.success(request, "Te has registrado correctamente!")
            return redirect("/account")


    return  redirect("/account")



