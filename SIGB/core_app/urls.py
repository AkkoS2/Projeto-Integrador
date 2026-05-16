from django.urls import path
from . import views


app_name="core_app"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("agenda", views.agenda, name="agenda"),
    path("historico", views.historico, name="historico"),
    path("bombeiros", views.bombeiros, name="bombeiros"),
    path("frotas", views.frotas, name="frotas"),
    path("escala", views.escalas, name="escalas")
]