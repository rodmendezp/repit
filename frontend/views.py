from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from Repit.settings import DEBUG
from repituser.forms import UserForm


def index(request):
    template_file = 'landing/index.webpack' + ('.dev' if DEBUG else '') + '.html'
    template = loader.get_template(template_file)
    print('in landing')
    response = HttpResponse(template.render({}))
    return response


@login_required(redirect_field_name=None, login_url='/accounts')
def app(request):
    template_file = 'app/index.webpack' + ('.dev' if DEBUG else '') + '.html'
    template = loader.get_template(template_file)
    print('in app')
    response = HttpResponse(template.render({}, request))
    return response


def auth(request):
    template_file = 'auth/auth.webpack' + ('.dev' if DEBUG else '') + '.html'
    template = loader.get_template(template_file)
    print('in auth')
    response = HttpResponse(template.render({}, request))
    return response


class AjaxableResponseMixin(object):
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            print('IS AJAX')
            return JsonResponse(form.errors, status=400)
        return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if type(response) is HttpResponseRedirect and self.request.is_ajax():
            return JsonResponse({'url': response.url}, status=response.status)
        elif self.request.is_ajax():
            return JsonResponse({'success': True}, status=200)
        return response


class EmailLoginView(AjaxableResponseMixin, LoginView):
    form_class = UserForm
    template_name = 'auth/auth.webpack' + ('.dev' if DEBUG else '') + '.html'
    redirect_authenticated_user = True
    # redirect_field_name = 'to'

    def __init__(self, *args, **kwargs):
        print('in login')


