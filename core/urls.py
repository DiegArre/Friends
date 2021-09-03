from django.urls import path 
from . import views


urlpatterns = [
    path("",views.inicio),
    path("friends",views.friends),
    path("friends/add/<int:add_id>",views.add_friend),
    path("friends/remove/<int:remove_id>",views.remove_friend),
    path("user/<int:user_id>", views.user)

]