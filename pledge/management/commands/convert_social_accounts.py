from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError

from allaccess.models import Provider, AccountAccess 


class Command(NoArgsCommand):
    "Convert existing signatures from django-social-auth to django-all-access."

    def handle_noargs(self, **options):
        try:
            from social_auth.models import UserSocialAuth
        except ImportError:
            raise CommandError("django-social-auth is not installed.")
        # Create providers if they don't already exist
        defaults = {
            'authorization_url': 'https://www.facebook.com/dialog/oauth',
            'access_token_url': 'https://graph.facebook.com/oauth/access_token',
            'profile_url': 'https://graph.facebook.com/me',
            'key': getattr(settings, 'FACEBOOK_APP_ID', None) or None,
            'secret': getattr(settings, 'FACEBOOK_API_SECRET', None) or None,
        }
        facebook, _ = Provider.objects.get_or_create(name='facebook', defaults=defaults)
        defaults = {
            'request_token_url': 'https://api.twitter.com/oauth/request_token',
            'authorization_url': 'https://api.twitter.com/oauth/authenticate',
            'access_token_url': 'https://api.twitter.com/oauth/access_token',
            'profile_url': 'https://twitter.com/account/verify_credentials.json',
            'key': getattr(settings, 'TWITTER_CONSUMER_KEY', None) or None,
            'secret': getattr(settings, 'TWITTER_CONSUMER_SECRET', None) or None,
        }
        twitter, _ = Provider.objects.get_or_create(name='twitter', defaults=defaults)
        for social in UserSocialAuth.objects.all():
            provider = None
            if social.provider == 'facebook':
                provider = facebook
            elif social.provider == 'twitter':
                provider = twitter
            if provider is not None:
                defaults = {
                    'user': social.user,
                }
                access, _ = AccountAccess.objects.get_or_create(
                    identifier=social.uid, provider=provider, defaults=defaults
                )
