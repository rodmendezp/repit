from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def is_user(request):
    if request.method == 'GET':
        user_model = get_user_model()
        try:
            validate_email(request.GET.get('email'))
        except ValidationError:
            return JsonResponse({'message': 'Invalid email.'}, status=400)
        try:
            user = user_model.objects.get(email=request.GET.get('email'))
            return JsonResponse({}, status=200)
        except user_model.DoesNotExist:
            return JsonResponse({}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request.'}, status=400)
