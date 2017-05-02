from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import status

from . import serializers
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.response import Response
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.forms import ValidationError
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
import json

from rest_framework import generics

from . import forms


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('app:login'))

@login_required
def landing(request):
    return render(request, 'app/landing.html')

# @login_required()
# def update_location(request):
#
#     lat = request.POST['lat']
#     lon = request.POST['long']
#
#     try:
#         user = get_user_model().objects.get( id = request.id)
#         user.


def login_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('app:landing'))
                else:
                    form.add_error(None, ValidationError(
                        "Your account is not active."
                    ))
            else:

                form.add_error(None, ValidationError(
                    "Invalid User Id of Password"
                ))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.LoginForm()

    return render(request, 'app/login.html', {'form': form})


def signup_view(request):
    if request.POST:
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = get_user_model().objects.get(email=email)
                if user:
                    form.add_error(None, ValidationError("This user already exists."))
            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_user(username=username)

                # Set user fields provided
                user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()

                return redirect(reverse('app:login'))
    else:
        form = forms.SignupForm()

    return render(request, 'app/signup.html', {'form': form})


class UserProfile(UpdateView):
    form_class = forms.UserProfileForm
    template_name = "app/user_profile.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfile, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return get_user_model().objects.get(pk=self.request.user.pk)

    def form_invalid(self, form):
        return super(UserProfile, self).form_invalid(form)


# def updateInfo(request):
#     if request.POST:
#         form = forms.insertGeo(request.POST)
#         if form.is_valid():
#             pnt = Point(form.cleaned_data['lat'],form.cleaned_data['long'])
#             # user = request.user
#             # id = user.id
#             print(request)
#             try:
#                 user = get_user_model(pk=request.user.pk)
#                 # Set user fields provided
#                 user.last_location = pnt
#                 user.update()
#
#                 return redirect(reverse('app:updateInfo'))
#             except:
#                 pass
#     else:
#             form = forms.insertGeo()
#
#     return render(request, 'app/user_profile.html', {'form': form})


# user update location with normal django view
@login_required
def updatelocat(request):
    if request.POST:
        user = get_user_model().objects.get(pk=request.user.pk)
        lat = float(request.POST.get("lat", False))
        long = float(request.POST.get("long", False))
        user.last_location = point = Point(long, lat)
        user.save(update_fields = ['last_location'])
        # print('1')
        return HttpResponse()


class listV(generics.ListAPIView):
    serializer_class = serializers.UserMeSerializer

    print('hihi')

    def get_queryset(self):
        # return get_user_model().objects.all().order_by("username")
        # serializer = serializers.UserMeSerializer(get_user_model().objects.all().order_by("username"))
        data = get_user_model().objects.all()
        sdata = serialize('json', list(data), fields=('username', 'id', 'last_location'))
        return get_user_model().objects.all().order_by("username")

    def get_object(self):
        return get_user_model().objects.get(email=self.request.user.email)

    def final_process(self):
        data = get_user_model().objects.all()
        sdata = serialize('json', list(data), fields=('username', 'id', 'last_location'))
        print('hahaha    '+data)
        print('seeeeeeee   '+sdata)

        return Response(sdata, status=status.HTTP_200_OK)
