from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.contrib import messages
from .models import Profile, CompanyProfile, InfluencerProfile
from .forms import ProfileForm, CompanyProfileForm, InfluencerProfileForm
from users.models import CustomUser

@login_required
def create_profile(request, user_type):
    # Verificar que el tipo de usuario coincida con el del usuario autenticado
    if request.user.user_type != user_type:
        messages.error(request, "No tienes permiso para crear este tipo de perfil.")
        return redirect('dashboard')
    
    # Verificar si el usuario ya tiene un perfil
    try:
        profile = request.user.profile
        messages.info(request, "Ya tienes un perfil creado.")
        return redirect('dashboard')
    except Profile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)
        
        if user_type == 'empresa':
            specific_form = CompanyProfileForm(request.POST)
        else:  # influencer
            specific_form = InfluencerProfileForm(request.POST)
        
        if profile_form.is_valid() and specific_form.is_valid():
            # Crear perfil base
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            
            # Crear perfil específico
            specific_profile = specific_form.save(commit=False)
            specific_profile.profile = profile
            specific_profile.save()
            
            messages.success(request, "¡Tu perfil ha sido creado exitosamente!")
            return redirect('dashboard')
    else:
        profile_form = ProfileForm()
        
        if user_type == 'empresa':
            specific_form = CompanyProfileForm()
        else:  # influencer
            specific_form = InfluencerProfileForm()
    
    context = {
        'profile_form': profile_form,
        'specific_form': specific_form,
        'user_type': user_type
    }
    return render(request, 'profiles/create_profile.html', context)

@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile  # Accede al perfil relacionado

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        profile.bio = request.POST.get('bio')
        profile.location = request.POST.get('location')
        profile.website = request.POST.get('website')
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        user.save()
        profile.save()
        return redirect('profiles:view_profile')  # Redirige a la página de perfil después de guardar

    return render(request, 'profiles/edit_profile.html', {'user': user})

@login_required
def view_profile(request):
    return render(request, 'profiles/view_profile.html', {
        'user': request.user,
        'company': getattr(request.user.profile, 'company', None),
        'influencer': getattr(request.user.profile, 'influencer', None),
    })

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

class CompanyListView(LoginRequiredMixin, ListView):
    model = CompanyProfile
    template_name = 'profiles/company_list.html'
    context_object_name = 'companies'
    
    def get_queryset(self):
        return CompanyProfile.objects.select_related('profile__user').all()

class InfluencerListView(LoginRequiredMixin, ListView):
    model = InfluencerProfile
    template_name = 'profiles/influencer_list.html'
    context_object_name = 'influencers'
    
    def get_queryset(self):
        return InfluencerProfile.objects.select_related('profile__user').all()

