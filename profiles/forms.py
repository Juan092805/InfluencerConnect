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
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['industry', 'company_size', 'logo']  # Agregado el campo 'logo'
        labels = {
            'industry': 'Industria',
            'company_size': 'Tamaño de la empresa',
            'logo': 'Logotipo de la empresa',
        }
        widgets = {
            'industry': forms.Select(attrs={'class': 'form-control'}),
            'company_size': forms.Select(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class InfluencerProfileForm(forms.ModelForm):
    class Meta:
        model = InfluencerProfile
        fields = ['category', 'platforms', 'audience_size', 'profile_photo', 'bio']  
        labels = {
            'category': 'Categoría principal',
            'platforms': 'Plataformas',
            'audience_size': 'Tamaño de audiencia',
            'profile_photo': 'Foto de perfil',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'platforms': forms.TextInput(attrs={'class': 'form-control'}),
            'audience_size': forms.Select(attrs={'class': 'form-control'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

