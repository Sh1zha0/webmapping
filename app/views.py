from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator

from django.forms import ValidationError
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView, UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from . import forms


@login_required
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect(reverse('app:login'))

@login_required
def landing(request):
    return render(request, 'app/landing.html')


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
                    # return form.form_invalid(form)

            else:
                form.add_error(None, ValidationError(
                    "Invalid User Id of Password"
                ))
                # messages.error(request=self.request, message=_("Invalid User Id of Password"))
                # return form.form_invalid(form)

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
                user = get_user_model().objects.get(username=username)
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
    # success_url = reverse('app:userprofile')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfile, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return get_user_model().objects.get(pk=self.request.user.pk)


# class ManageProfile(SuccessMessageMixin, UpdateView):
#     template_name = 'Users/manage_profile.html'
#     form_class = forms.UserProfileForm
#     success_message = _("Profile Updated.")
#
#     # fields = ['first_name', 'last_name', 'phone_number', 'gender', 'age_range', 'photo', 'timezone', ]
#
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(ManageProfile, self).dispatch(*args, **kwargs)
#
#     def get_object(self):
#         return get_object_or_404(models.UserProfile, pk=self.request.user.pk)
#
#     def form_valid(self, form):
#         phone_number = form.cleaned_data['phone_number']
#         if not parsed_phone_number(self.request, phone_number):
#             messages.error(self.request,
#                            _("Your Phone number appears to be invalid. If you enter this without the country code, "
#                              "we'll try to locate the number using your current location. If we cannot do this you will "
#                              "need to enter it with the country code. See the help text [i] for more information."))
#             return self.form_invalid(form)
#
#         image = form.cleaned_data.get('photo', None)
#         if image:
#             if image.size > 5 * 1024 * 1024:
#                 messages.error(self.request,
#                                _("The image is too large. The size limit is 5Mb. Please upload a smaller image."))
#                 return self.form_invalid(form)
#                 # raise forms.ValidationError(_("Image file too large ( > 5mb )"))
#                 # return image
#         # else:
#         #     raise forms.ValidationError(_("Couldn't read uploaded image"))
#
#         if not form.instance.profile_updated:
#             form.instance.profile_updated = True
#         return super(ManageProfile, self).form_valid(form)
#
#     def form_invalid(self, form):
#         message = show_form_errors(form)
#         if message:
#             messages.error(self.request, message, extra_tags="safe")
#         return super(ManageProfile, self).form_invalid(form)
#
#     def get_success_url(self):
#         return reverse('users:manage_profile')
