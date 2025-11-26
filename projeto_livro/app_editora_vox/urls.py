from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_livros, name='lista_livros'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('livro/criar/', views.criar_livro, name='criar_livro'),
    path('livro/<int:livro_id>/editar/', views.editar_livro, name='editar_livro'),
]
