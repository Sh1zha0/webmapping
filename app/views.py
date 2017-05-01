from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
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
import json

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

@login_required
def updatelocat(request):
    if request.POST:
        user = get_user_model().objects.get(pk=request.user.pk)
        # # user.update()
        # user.last_location = GEOSGeometry(geo)
        geoS = request.POST
        # geoS = serialize('geojson', request.POST);
        print(geoS);
        # user.save(update_fields = ['last_location'])
        # print('1')
        return HttpResponse()

