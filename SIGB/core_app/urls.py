from django.urls import path
from . import views


app_name="core_app"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("agenda", views.agenda, name="agenda"),
    path("historico", views.historico, name="historico"),
    path("bombeiros", views.bombeiros, name="bombeiros"),
    path("manutencoes", views.manutencoes, name="manutencoes"),
    path("viaturas", views.viaturas, name="viaturas"),
    path("escala", views.escalas, name="escalas")
]