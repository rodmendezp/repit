import datetime

from django.http import HttpResponse
from django.utils import timezone
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm


def index(request):
    datetime_time = datetime.datetime.now()
    time = timezone.now()
    time_local = timezone.localtime()
    return HttpResponse("timezone.now() = " + str(time) + "\n datetime.now() = " + str(datetime_time) +
                        "\n time_local = " + str(time_local))


class UserFormView(View):
    form_class = UserForm
    template_name = 'repituser/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Creates an object from the form, but does not save it to the database
            user = form.save(commit=False)

            # Normalize values and use hashing function to encrypt password
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Returns User object if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('label:index')

        # If form not valid or user is inactive then redirect to the same form
        return render(request, self.template_name, {'form': form})