from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Campaign, Application, Comment, CampaignView, Response
from .forms import CampaignForm, ApplicationForm, ResponseForm

@login_required
def campaign_list(request):
    query = request.GET.get('q')  # Obtén la palabra clave de la búsqueda
    if request.user.user_type == 'empresa':
        campaigns = Campaign.objects.filter(company=request.user)
    else:
        if query:
            campaigns = Campaign.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)  # Cambiado 'title' por 'name'
            )
        else:
            campaigns = Campaign.objects.all()

    for campaign in campaigns:
        # Verificar si el usuario ya ha visto esta campaña
        if not CampaignView.objects.filter(campaign=campaign, user=request.user).exists():
            # Registrar la vista y aumentar el contador
            CampaignView.objects.create(campaign=campaign, user=request.user)
            campaign.views += 1
            campaign.save()

    return render(request, 'campaigns/campaign_list.html', {'campaigns': campaigns})

@login_required
def campaign_create(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.company = request.user
            campaign.save()
            return redirect('campaigns:campaign_list')
    else:
        form = CampaignForm()
    return render(request, 'campaigns/campaign_create.html', {'form': form})

@login_required
def campaign_edit(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id, company=request.user)

    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return redirect('campaigns:campaign_list')
    else:
        form = CampaignForm(instance=campaign)

    return render(request, 'campaigns/campaign_edit.html', {'form': form, 'campaign': campaign})

@login_required
def apply_to_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    if request.user.user_type != 'influencer':
        return redirect('campaigns:campaign_list')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.campaign = campaign
            application.influencer = request.user
            application.save()
            return redirect('campaigns:campaign_list')
    else:
        form = ApplicationForm()
    return render(request, 'campaigns/apply_to_campaign.html', {'form': form, 'campaign': campaign})

@login_required
def campaign_applications(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id, company=request.user)
    applications = campaign.applications.all()  # Relación inversa desde Application
    return render(request, 'campaigns/campaign_applications.html', {
        'campaign': campaign,
        'applications': applications,
    })

@login_required
def like_campaign(request, campaign_id):
    if request.method == 'POST':
        campaign = get_object_or_404(Campaign, id=campaign_id)
        campaign.likes += 1
        campaign.save()
        return JsonResponse({'likes': campaign.likes})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def respond_to_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    # Verificar que el usuario sea parte de la conversación
    if request.user != application.campaign.company and request.user != application.influencer:
        return redirect('campaigns:campaign_list')

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.application = application
            response.user = request.user
            response.save()
            return redirect('campaigns:respond_to_application', application_id=application.id)
    else:
        form = ResponseForm()

    return render(request, 'campaigns/respond_to_application.html', {
        'form': form,
        'application': application,
        'responses': application.responses.all()
    })

@login_required
def influencer_applications(request):
    # Filtrar las postulaciones del influencer actual
    applications = Application.objects.filter(influencer=request.user)

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.application = get_object_or_404(Application, id=request.POST.get('application_id'))
            response.save()
            return redirect('campaigns:influencer_applications')
    else:
        form = ResponseForm()

    return render(request, 'campaigns/influencer_applications.html', {
        'applications': applications,
        'form': form
    })