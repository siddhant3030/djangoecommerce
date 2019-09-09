"""
Allow Satchmo to use an email address instead of the user id as the
primary id
Taken from a posting on the Django mailing list.
Thanks to Vasily Sulatskov for sending this to the list.
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
import re

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain
            
class EmailBackend(ModelBackend):
    """Authenticate using email only"""
    def authenticate(self, *args, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        #If username is an email address, then try to pull it up
        if username and password and email_re.search(username):
            try:
                user = User.objects.filter(email__iexact=username)[0]
                if user.check_password(password):
                    return user
            except IndexError:
                pass
        return None
            
