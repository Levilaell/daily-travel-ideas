# views.py

from rest_framework import viewsets
from .models import Post, Idea, Theme
from .serializers import PostSerializer, ThemeSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Case, When  # Import necessário para preservar a ordem

class HomeView(ListView):
    model = Post
    template_name = 'blog/home.html'  # Caminho para o template
    context_object_name = 'posts'  # Nome da variável no template
    paginate_by = 10  # Número de postagens por página (opcional)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.objects.order_by('-created_at')[:5]
        
        # Especificar os slugs dos temas que você quer exibir
        theme_slugs = ['travel-ideas', 'gastronomy-ideas', 'home-decor-ideas', 'tech-trends']
        
        # Preservar a ordem dos temas
        preserved = Case(*[When(slug=slug, then=pos) for pos, slug in enumerate(theme_slugs)])
        themes = Theme.objects.filter(slug__in=theme_slugs).order_by(preserved)
        
        context['themes'] = themes  # Adiciona os temas específicos ao contexto
        print(context['themes'])
        return context
    
    def get_queryset(self):
        # Ordena a lista principal de posts pelos mais recentes
        return Post.objects.order_by('-created_at')
    
class BlogView(ListView):
    model = Post
    template_name = 'blog/blog.html'  # Caminho para o template
    context_object_name = 'posts'  # Nome da variável no template
    paginate_by = 10  # Número de postagens por página (opcional)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_posts'] = Post.objects.order_by('-views')[:5]
        print(context)  # Linha de depuração
        return context
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'

    def get_object(self):
        post = super().get_object()
        post.views += 1
        post.save()
        return post

class ThemePostListView(ListView):
    model = Post
    template_name = 'blog/theme-posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        theme_slug = self.kwargs['slug']
        return Post.objects.filter(themes__slug=theme_slug).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theme_slug = self.kwargs['slug']
        context['theme'] = get_object_or_404(Theme, slug=theme_slug)
        return context
    
class AboutView(TemplateView):
    template_name = 'blog/about.html'  # Caminho para o template da página sobre


class PrivacyPolicyView(TemplateView):
    template_name = 'blog/privacy-policy.html'  # Caminho para o template da política de privacidade


class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search-results.html'  # Caminho para o template de resultados de pesquisa
    context_object_name = 'posts'  # Nome da variável no template

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ) if query else Post.objects.none()

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        """
        Sobrescreve o método create para garantir que a resposta inclui o campo 'link'
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['slug']
