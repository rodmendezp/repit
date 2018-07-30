import pytz
import datetime

from django.http import HttpResponse
from django.utils import timezone


def index(request):
    datetime_time = datetime.datetime.now()
    time = timezone.now()
    time_local = timezone.localtime()
    return HttpResponse("timezone.now() = " + str(time) + "\n datetime.now() = " + str(datetime_time) +
                        "\n time_local = " + str(time_local))
