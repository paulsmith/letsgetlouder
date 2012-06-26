import random
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from pledge.models import Signee


class BaseTestCase(TestCase):
    "Common helper methods for testing pledge functionality."

    def get_random_string(self, length=10):
        "Create a random string for generating test data."
        return ''.join(random.choice(string.ascii_letters) for x in xrange(length))

    def get_random_email(self, domain='example.com'):
        "Create a random email for generating test data."
        local = self.get_random_string()
        return '{0}@{1}'.format(local, domain)
    
    def get_random_url(self, domain='example.com'):
        "Create a random url for generating test data."
        path = self.get_random_string()
        return 'http://{0}/{1}'.format(domain, path)

    def create_user(self, **kwargs):
        "Create a test User"
        defaults = {
            'username': self.get_random_string(),
            'password': self.get_random_string(),
            'email': self.get_random_email()
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)


class SignPledgeTestCase(BaseTestCase):
    "View to sign the pledge."

    def setUp(self):
        self.username = 'test'
        self.password = 'abc'
        self.user = self.create_user(username=self.username, password=self.password)
        self.pledge = self.user.get_profile()
        self.pledge.signed = False
        self.pledge.save()
        self.client.login(username=self.username, password=self.password)
        self.url = reverse('sign-pledge')
        self.account_url = reverse('account')

    def test_login_required(self):
        "User must be authenticated to sign the pledge."
        self.client.logout()
        response = self.client.post(self.url)
        self.assertRedirects(response, settings.LOGIN_URL + '?next=' + self.url)

    def test_successful_sign(self):
        "Successfully sign the pledge."
        response = self.client.post(self.url)
        self.assertRedirects(response, self.account_url)
        pledge = Signee.objects.get(pk=self.pledge.pk)
        self.assertTrue(pledge.signed, "Pledge should now be signed.")

    def test_non_post(self):
        "No action take on GET. Send user back to the account page."
        response = self.client.get(self.url)
        self.assertRedirects(response, self.account_url)
        pledge = Signee.objects.get(pk=self.pledge.pk)
        self.assertFalse(pledge.signed, "Pledge not signed.")

    def test_already_signed(self):
        "User has already signed the pledge. No real change."
        self.pledge.signed = True
        self.pledge.save()
        response = self.client.post(self.url)
        self.assertRedirects(response, self.account_url)
        pledge = Signee.objects.get(pk=self.pledge.pk)
        self.assertTrue(pledge.signed, "Pledge should still be signed.")


class UnSignPledgeTestCase(BaseTestCase):
    "View to unsign the pledge."

    def setUp(self):
        self.username = 'test'
        self.password = 'abc'
        self.user = self.create_user(username=self.username, password=self.password)
        self.pledge = self.user.get_profile()
        self.pledge.signed = True
        self.pledge.save()
        self.client.login(username=self.username, password=self.password)
        self.url = reverse('unsign-pledge')
        self.account_url = reverse('account')

    def test_login_required(self):
        "User must be authenticated to sign the pledge."
        self.client.logout()
        response = self.client.post(self.url)
        self.assertRedirects(response, settings.LOGIN_URL + '?next=' + self.url)

    def test_successful_unsign(self):
        "Successfully unsign the pledge."
        response = self.client.post(self.url)
        self.assertRedirects(response, self.account_url)
        pledge = Signee.objects.get(pk=self.pledge.pk)
        self.assertFalse(pledge.signed, "Pledge should no longer be signed.")

    def test_non_post(self):
        "No action take on GET. Send user back to the account page."
        response = self.client.get(self.url)
        self.assertRedirects(response, self.account_url)
        pledge = Signee.objects.get(pk=self.pledge.pk)
        self.assertTrue(pledge.signed, "Pledge still signed.")

    def test_already_unsigned(self):
        "User has already unsigned the pledge. No real change."
        self.pledge.signed = False
        self.pledge.save()
        response = self.client.post(self.url)
        self.assertRedirects(response, self.account_url)
        pledge = Signee.objects.get(pk=self.pledge.pk)
        self.assertFalse(pledge.signed, "Pledge should still be unsigned.")
