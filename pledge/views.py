from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from pledge.models import Signee


@login_required
def sign_view(request):
    if request.method == 'POST':
        Signee.objects.filter(user=request.user).update(signed=True)
    return redirect('/account/')


@login_required
def unsign_view(request):
    if request.method == 'POST':
        Signee.objects.filter(user=request.user).update(signed=False)
    return redirect('/account/')
