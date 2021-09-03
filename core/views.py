from django.shortcuts import redirect, render
from account.models import User
# Create your views here.


def inicio(request):
    if "usuario" in request.session:
       return redirect("/friends")
    else: return redirect ("/account")

def friends(request):
    user = User.objects.get(id = request.session["usuario"]["id"])
    friends = user.amigos.all()
    print(friends)
    nofriendsobject =set(User.objects.all()) - set(user.amigos.all())
    try: 
        nofriendsobject.remove(user)
    except:
        pass
    nofriends = list(nofriendsobject)

    # if len(friends) > 0:
    #     mostrar = True
    # else : mostrar = False

    context ={
        # "mostrar" : mostrar,
        "amigos" : friends,
        "noamigos" : nofriends
    }

    return render(request, "core/friends.html",context)


def add_friend(request,add_id):
    add = User.objects.get(id = add_id)
    user = User.objects.get(id = request.session["usuario"]["id"])

    user.amigos.add(add)
    add.amigos.add(user)

    return redirect("/")

def remove_friend(request,remove_id):
    remove = User.objects.get(id = remove_id)
    user = User.objects.get(id = request.session["usuario"]["id"])

    user.amigos.remove(remove)
    remove.amigos.remove(user)

    return redirect("/")



def user(request,user_id):

    user = User.objects.filter(id = user_id)
    if len(user) > 0:

        context = {
            "alias" : user[0].alias,
            "nombre" : user[0].nombre,
            "email" : user[0].email
        }

    return render(request, "core/user.html", context)