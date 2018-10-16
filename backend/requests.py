from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from backend.tokens import account_activation_token


def user_activation(request, uidb64, token):
    if request.method == 'GET':
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user_model = get_user_model()
            user = user_model.objects.get(pk=uid)
        except Exception as e:
            return HttpResponseNotFound
        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
    return redirect('/')


def is_user(request):
    if request.method == 'GET':
        user_model = get_user_model()
        try:
            validate_email(request.GET.get('email'))
        except ValidationError:
            return JsonResponse({'message': 'Invalid email.'}, status=400)
        try:
            user_model.objects.get(email=request.GET.get('email'))
            return JsonResponse({}, status=200)
        except user_model.DoesNotExist:
            return JsonResponse({}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request.'}, status=400)
