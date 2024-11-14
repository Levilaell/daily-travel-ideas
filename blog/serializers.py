from rest_framework import serializers, viewsets
from .models import Post, Idea, Theme
from rest_framework.reverse import reverse
import json

class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ['title', 'description', 'image_url']

class PostSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    ideas = IdeaSerializer(many=True, required=False)
    themes = serializers.SlugRelatedField(
        many=True,
        queryset=Theme.objects.all(),
        slug_field='slug',
        required=False,
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'main_description', 'meta_description', 'featured_image', 'created_at', 'link', 'ideas', 'themes']
        read_only_fields = ['id', 'created_at', 'link']

    def get_link(self, obj):
        request = self.context.get('request')
        return reverse('post-detail', kwargs={'slug': obj.slug}, request=request)

    def create(self, validated_data):
        # Extrair ideias do initial_data em vez de validated_data
        ideas_data = self.initial_data.get('ideas', '[]')
        print("Received ideas data:", ideas_data)

        # Analisar a string JSON em uma lista de dicionários
        if isinstance(ideas_data, str):
            ideas_data = json.loads(ideas_data)
            print("Parsed ideas data:", ideas_data)
        else:
            print("ideas_data is not a string")

        # Extrair os temas do validated_data
        themes_data = validated_data.pop('themes', None)

        # Criar a instância do Post
        post = Post.objects.create(**validated_data)

        # Atribuir temas ao post se houver
        if themes_data:
            post.themes.set(themes_data)

        # Criar instâncias de Idea
        for idea_data in ideas_data:
            Idea.objects.create(post=post, **idea_data)
        return post

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'name', 'slug', 'image']
        read_only_fields = ['id', 'slug']
