from django.contrib.auth import logout
from django.shortcuts import redirect, render

from pledge.models import Signee

def index_view(request):
    signees = Signee.objects.filter(signed=True).order_by('-when').\
                select_related('user')
    signees = [s.user for s in signees]
    return render(request, 'index.html', {
        'signees': signees,
    })

def sign_view(request):
    signee = request.user.get_profile()
    signee.signed = True
    signee.save()
    return redirect('/account/')

def unsign_view(request):
    signee = request.user.get_profile()
    signee.signed = False
    signee.save()
    return redirect('/account/')

def logout_view(request):
    logout(request)
    return redirect('/')
