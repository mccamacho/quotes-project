from django.urls import path
from quotes_app import views

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("quotes", views.dashboard),
    path("addquote", views.addquote),
    path("logout", views.logout),
    path("user/<int:number>", views.showuser),
    path("quotes/<int:number>", views.editquote),
    path("delete/<int:number>",views.delete),
    path("<int:number>/updateshow", views.update),
    path("<int:number>/addfavorites", views.addtofavorite),
    path("<int:number>/removefavorite", views.removefromfavorite),
]
