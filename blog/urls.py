# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HomeView, BlogView, PostDetailView, AboutView, PrivacyPolicyView,
    SearchResultsView, ThemePostListView, PostViewSet, ThemeViewSet
)

# Roteador para a API
router = DefaultRouter()
router.register(r'api_posts', PostViewSet, basename='api_post')
router.register(r'themes', ThemeViewSet)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Página inicial
    # path('blog/', BlogView.as_view(), name='blog'),  # Lista de posts (se necessário)
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),  # Detalhes do post
    path('about/', AboutView.as_view(), name='about'),  # Página Sobre
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),  # Política de Privacidade
    path('search/', SearchResultsView.as_view(), name='search-results'),  # Resultados da busca
    path('theme/<slug:slug>/', ThemePostListView.as_view(), name='theme-posts'),  # Posts por tema

    # URLs da API sob 'api/'
    path('api/', include(router.urls)),
]
