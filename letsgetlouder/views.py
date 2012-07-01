from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

from allaccess.views import OAuthRedirect, OAuthCallback

from pledge.models import Signee


def index_view(request):
    signees = Signee.objects.filter(signed=True).order_by('-when').\
                select_related('user')
    signees = [s.user for s in signees]
    return render(request, 'index.html', {
        'signees': signees,
    })


def logout_view(request):
    logout(request)
    return redirect('/')


class LoginRedirect(OAuthRedirect):
    "Request additional permissions."

    def get_additional_parameters(self, provider):
        "Request additional permissions for FB users."
        if provider.name == 'facebook':
            # Request permission to see user's email
            return {'scope': 'email'}
        if provider.name == 'google':
            # Request permission to see user's profile and email
            perms = ['userinfo.email', 'userinfo.profile']
            scope = ' '.join(['https://www.googleapis.com/auth/' + p for p in perms])
            return {'scope': scope}
        return super(LoginRedirect, self).get_additional_parameters(provider)

    def get_callback_url(self, provider):
        "Point callback to customized view name."
        return reverse('login-callback', kwargs={'provider': provider.name})


class LoginCallback(OAuthCallback):
    "Customization to default django-all-access callback."

    def get_or_create_user(self, provider, access, info):
        "Update newly created user using their profile information."
        user = super(LoginCallback, self).get_or_create_user(provider, access, info)
        update = {}
        if provider.name == 'facebook':
            update['first_name'] = info.get('first_name', '')
            update['last_name'] = info.get('last_name', '')
            update['email'] = info.get('email', '')
        elif provider.name == 'twitter':
            # According the to Twitter docs this can only be 20 characters
            # so it will fit in just the first_name field.
            # https://dev.twitter.com/docs/api/1/post/account/update_profile
            update['first_name'] = info.get('name', '')
            update['last_name'] = ''
        elif provider.name == 'google':
            update['first_name'] = info.get('given_name', '')
            update['last_name'] = info.get('family_name', '')
            update['email'] = info.get('email', '')
        for field, value in update.items():
            setattr(user, field, value)
            user.save()
        return user
