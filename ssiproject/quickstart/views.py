from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickstart.serializers import UserSerializer, GroupSerializer, VisitSerializer
from quickstart.models import Visit
from rest_framework import permissions
from rest_framework import generics
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from quickstart.permissions import IsOwnerOrReadOnly
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.views.generic.list import ListView
from quickstart import models
from quickstart.models import Visit, PatientProfile, DoctorProfile
from quickstart.forms import PatientProfileForm, UserForm, VisitFormP, VisitFormD
from django.db import transaction
import datetime
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'visits': reverse('visits', request=request, format=format)
    })

class VisitViewSet(viewsets.ModelViewSet):
	queryset = Visit.objects.all()
	serializer_class = VisitSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
    return render_to_response('login.html')
	
def start_page(request):
    if request.user.is_authenticated():return render_to_response('main.html', {'user': request.user})
    else: return render_to_response('index.html')

def main(request):
	if request.user.is_authenticated():
		userProfile = PatientProfile.objects.filter(user=request.user)
		if userProfile: 
			context= {
				'profiles': userProfile
			}
			return render(request, 'main.html', context)
		userProfile = DoctorProfile.objects.filter(user=request.user)
		if userProfile: return render(userProfile, 'main.html')
		else: return redirect('/accounts/login')
	else: return redirect('/accounts/login')

	
def visits(request):
	if request.user.is_authenticated():
		user = PatientProfile.objects.filter(user= request.user)
		if not user[0]:#dla doktora
			user = DoctorProfile.objects.filter(user= request.user)
			visitsQuery = Visit.objects.filter(doctor=user)
			visit_form = VisitFormD(request.POST)
			if request.method == 'POST' and visit_form.is_valid():
				Visit.objects.create(date = visit_form.cleaned_data['date'], title = visit_form.cleaned_data['title'], desc = visit_form.cleaned_data['desc'], owner = visit_form.cleaned_data['owner'], doctor = user[0])
			return render(request, 'visits.html', {'visits':visitsQuery, 'visit_form': visit_form})
		else:
			visitsQuery = Visit.objects.filter(owner=user)
			visit_form = VisitFormP(request.POST)
			if request.method == 'POST' and visit_form.is_valid():
				Visit.objects.create(date = visit_form.cleaned_data['date'], title = visit_form.cleaned_data['title'], desc = visit_form.cleaned_data['desc'], doctor = visit_form.cleaned_data['doctor'], owner = user[0])
			return render(request, 'visits.html', {'visits':visitsQuery, 'visit_form': visit_form})
	else : return redirect('/accounts/login')
	
def signup(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		profile_form = PatientProfileForm(request.POST)
		if user_form.is_valid() and profile_form.is_valid():
	
			user = User.objects.create_user(user_form.cleaned_data['username'],user_form.cleaned_data['email'],user_form.cleaned_data['password1'])
			user.first_name = user_form.cleaned_data['first_name']
			user.last_name = user_form.cleaned_data['last_name']
			user.save()
			PatientProfile.objects.filter(user = user).update(pesel = profile_form.cleaned_data['pesel'], isMale = profile_form.cleaned_data['isMale'], phone = profile_form.cleaned_data['phone'], birth = profile_form.cleaned_data['birth'] )
			raw_password = user_form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return main(request)
	else:
		user_form = UserForm()
		profile_form = PatientProfileForm()
		return render(request, 'signup.html', {'user_form': user_form,'profile_form': profile_form})
@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = PatientProfileForm(request.POST, instance=request.user.patientprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = PatientProfileForm(instance=request.user.patientprofile)
    return render(request, 'main.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })