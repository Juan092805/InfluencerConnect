from django import forms
from .models import Profile, CompanyProfile, InfluencerProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'website', 'location']
        labels = {
            'profile_picture': 'Foto de perfil',
            'bio': 'Descripción',
            'website': 'Sitio web',
            'location': 'Ubicación',
        }

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['industry', 'company_size']
        labels = {
            'industry': 'Industria',
            'company_size': 'Tamaño de la empresa',
        }

class InfluencerProfileForm(forms.ModelForm):
    class Meta:
        model = InfluencerProfile
        fields = ['category', 'platforms', 'audience_size']
        labels = {
            'category': 'Categoría principal',
            'platforms': 'Plataformas',
            'audience_size': 'Tamaño de audiencia',
        }

