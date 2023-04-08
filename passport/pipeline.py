from django.db.models import signals
from django.dispatch import Signal
from social.pipeline.user import *
from django.contrib.auth.models import User, Group
from social.utils import module_member

def new_users_handler(sender, user, response, details, **kwargs):
    user.groups.add(Group.objects.get(name='candidates'))

user_details.connect(new_users_handler, sender=None)