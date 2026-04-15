from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Article
from .forms import ArticleForm


# --- Solo requiere login ---
@login_required
def article_list(request):
    """Cualquier usuario autenticado puede ver la lista."""
    if request.user.has_perm('blog.publish_article'):
        articles = Article.objects.all()
    else:
        articles = Article.objects.filter(published=True)
    return render(request, 'blog/article_list.html', {'articles': articles})


# --- Requiere permiso específico ---
@permission_required('blog.add_article', raise_exception=True)
def article_create(request):
    """Solo usuarios con permiso 'add_article' pueden crear."""
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Artículo creado.')
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})


# --- Requiere login + permiso (combinados) ---
@login_required
@permission_required('blog.delete_article', raise_exception=True)
def article_delete(request, pk):
    """Solo usuarios con permiso 'delete_article' pueden eliminar."""
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Artículo eliminado.')
        return redirect('article_list')
    return render(request, 'blog/article_confirm_delete.html', {'article': article})


# --- Permiso personalizado ---
@permission_required('blog.publish_article', raise_exception=True)
def article_publish(request, pk):
    """Solo Editores pueden publicar artículos."""
    article = get_object_or_404(Article, pk=pk)
    article.published = True
    article.save()
    messages.success(request, f'"{article.title}" ha sido publicado.')
    return redirect('article_list')

@permission_required('blog.change_article', raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'blog/article_form.html', {'form': form})