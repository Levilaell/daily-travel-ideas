from django.db import models
from django.utils.text import slugify

from django.db import models
from django.utils.text import slugify

class Theme(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='theme_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Theme, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=155, blank=True, null=True)
    main_description = models.TextField()
    content = models.TextField()  # Conteúdo completo do post
    featured_image = models.ImageField(upload_to='featured_images/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    themes = models.ManyToManyField(Theme, related_name='posts', blank=True)  # Adiciona o relacionamento com Theme

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            unique_slug = self.slug
            num = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{num}"
                num += 1
            self.slug = unique_slug
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    
class Idea(models.Model):
    post = models.ForeignKey(Post, related_name='ideas', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)  # Título da ideia (por exemplo, "1. Nome da Ideia")
    description = models.TextField()  # Descrição da ideia
    image_url = models.URLField(max_length=500, blank=True, null=True)  # URL da imagem

    def __str__(self):
        return f"{self.title} - {self.post.title}"