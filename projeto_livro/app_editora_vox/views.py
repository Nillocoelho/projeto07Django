from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django import forms

from .forms import SignUpForm
from .models import Livro


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['ISBN', 'titulo', 'publicacao', 'preco', 'estoque', 'editora']
        labels = {
            'ISBN': 'ISBN',
            'titulo': 'Título',
            'publicacao': 'Data de Publicação',
            'preco': 'Preço',
            'estoque': 'Estoque',
            'editora': 'Editora',
        }


def lista_livros(request):
	"""Renderiza a listagem de livros com paginacao simples."""
	queryset = Livro.objects.select_related('editora').order_by('titulo')
	paginator = Paginator(queryset, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'page_obj': page_obj,
	}
	return render(request, 'app_editora_vox/livro_list.html', context)


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('lista_livros')
	else:
		form = SignUpForm()
	return render(request, 'app_editora_vox/signup.html', {'form': form})


def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('lista_livros')
	else:
		form = AuthenticationForm()
	return render(request, 'app_editora_vox/login.html', {'form': form})


def logout_view(request):
	logout(request)
	return redirect('login')


@login_required
def criar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_livros')
    else:
        form = LivroForm()
    return render(request, 'app_editora_vox/criar_livro.html', {'form': form})


@login_required
def editar_livro(request, livro_id):
    livro = Livro.objects.get(pk=livro_id)
    if request.method == 'POST':
        form = LivroForm(request.POST, instance=livro)
        if form.is_valid():
            form.save()
            return redirect('lista_livros')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'app_editora_vox/editar_livro.html', {'form': form})
