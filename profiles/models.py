from django.db import models
from django.conf import settings
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg')  # Ajuste en la ruta predeterminada
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def get_absolute_url(self):
        return reverse('profiles:profile_detail', kwargs={'pk': self.pk})

class CompanyProfile(models.Model):
    INDUSTRY_CHOICES = (
        ('tecnologia', 'Tecnología'),
        ('moda', 'Moda y Belleza'),
        ('alimentos', 'Alimentos y Bebidas'),
        ('salud', 'Salud y Bienestar'),
        ('viajes', 'Viajes y Turismo'),
        ('entretenimiento', 'Entretenimiento'),
        ('educacion', 'Educación'),
        ('otro', 'Otro'),
    )
    
    SIZE_CHOICES = (
        ('1-10', '1-10 empleados'),
        ('11-50', '11-50 empleados'),
        ('51-200', '51-200 empleados'),
        ('201-500', '201-500 empleados'),
        ('501+', '501+ empleados'),
    )
    
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='company')
    industry = models.CharField(max_length=20, choices=INDUSTRY_CHOICES)
    company_size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    description = models.TextField(blank=True)  # Descripción adicional de la empresa
    
    def __str__(self):
        return f'{self.profile.user.username} Company Profile'

class InfluencerProfile(models.Model):
    CATEGORY_CHOICES = (
        ('moda', 'Moda'),
        ('belleza', 'Belleza'),
        ('fitness', 'Fitness y Salud'),
        ('viajes', 'Viajes'),
        ('comida', 'Comida'),
        ('tecnologia', 'Tecnología'),
        ('gaming', 'Gaming'),
        ('lifestyle', 'Lifestyle'),
        ('otro', 'Otro'),
    )
    
    AUDIENCE_SIZE_CHOICES = (
        ('micro', 'Micro (1K-10K seguidores)'),
        ('pequeno', 'Pequeño (10K-50K seguidores)'),
        ('medio', 'Medio (50K-100K seguidores)'),
        ('grande', 'Grande (100K-500K seguidores)'),
        ('macro', 'Macro (500K-1M seguidores)'),
        ('mega', 'Mega (1M+ seguidores)'),
    )
    
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='influencer')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    platforms = models.CharField(max_length=200)
    audience_size = models.CharField(max_length=10, choices=AUDIENCE_SIZE_CHOICES)
    profile_photo = models.ImageField(upload_to='influencer_profiles/', blank=True, null=True)
    bio = models.TextField(blank=True) 
    
    def __str__(self):
        return f'{self.profile.user.username} Influencer Profile'

