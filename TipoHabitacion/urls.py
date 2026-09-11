from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<str:modelo>/', views.listar, name='listar'),
    path('<str:modelo>/crear/', views.crear, name='crear'),
    path('<str:modelo>/<int:pk>/', views.detalle, name='detalle'),
    path('<str:modelo>/<int:pk>/editar/', views.editar, name='editar'),
    path('<str:modelo>/<int:pk>/eliminar/', views.eliminar, name='eliminar'),
    path('<str:modelo>/exportar/excel/', views.exportar_excel, name='exportar_excel'),
    path('<str:modelo>/exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),
]
