from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, SuccessURLAllowedHostsMixin
from django.views.generic.edit import CreateView
from Repit.settings import DEBUG
from backend.forms import RegisterForm, LoginEmailForm


def index(request):
    template_file = 'landing/index.webpack' + ('.dev' if DEBUG else '') + '.html'
    template = loader.get_template(template_file)
    response = HttpResponse(template.render({}))
    return response


@login_required(redirect_field_name=None, login_url='/accounts/')
def app(request):
    template_file = 'app/index.webpack' + ('.dev' if DEBUG else '') + '.html'
    template = loader.get_template(template_file)
    response = HttpResponse(template.render({}, request))
    return response


def auth(request):
    template_file = 'auth/auth.webpack' + ('.dev' if DEBUG else '') + '.html'
    template = loader.get_template(template_file)
    response = HttpResponse(template.render({}, request))
    return response


class AjaxableResponseMixin(object):
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if hasattr(self, 'request') and self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if type(response) is HttpResponseRedirect and self.request.is_ajax():
            return JsonResponse({'url': response.url}, status=response.status_code)
        elif self.request.is_ajax():
            return JsonResponse({'success': True}, status=200)
        return response


class UserCreate(AjaxableResponseMixin, SuccessURLAllowedHostsMixin, CreateView):
    form_class = RegisterForm
    template_name = 'auth/auth.webpack' + ('.dev' if DEBUG else '') + '.html'
    success_url = '/'


class EmailLoginView(AjaxableResponseMixin, LoginView):
    form_class = LoginEmailForm
    template_name = 'auth/auth.webpack' + ('.dev' if DEBUG else '') + '.html'
    redirect_authenticated_user = True
    redirect_field_name = 'to'
