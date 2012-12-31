from django.conf import settings


def heroku(request):
    "Detect whether we are currently running on Heroku or not."
    return {'heroku': getattr(settings, 'HEROKU', False)}
