from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Comment
from datetime import datetime
from .filters import PostFilter
from .models import Post
from .forms import PostForm


class PostList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'flatpages/products.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'product.html'
    context_object_name = 'post'

class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CommentList(ListView):
    model = Comment
    template_name = 'flatpages/products.html'
    context_object_name = 'comments'

class CommentDetail(DetailView):
    model = Comment
    template_name = 'product.html'
    context_object_name = 'comment'


