from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings

from z.saas.models import Account
from z.auth.zuser.models import ZUser
from z.core.app.models import App, AppRegistration
from z.core.logo.models import Logo
from data.initial_data import root
import os

class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        # Create a first 'root' account
        zaccount, created = Account.objects.get_or_create(login=root.account['login'], \
                                                        name=root.account['name'])
        if created:
            zaccount.save()

            logo_filename = root.account['logo_file']
            print (logo_filename)
            if os.path.exists(logo_filename):
                print ("file exists")
                import shutil
                new_filename = os.path.join(settings.ACCOUNT_DATA_ROOT, "%s/logos/logo_%s.png" %(zaccount.login, zaccount.login))
                shutil.copy(logo_filename, new_filename)
                l = Logo(account=zaccount, title="logo %s" %(zaccount.name))
                #l.image = new_filename
                l.image = new_filename
                l.save()
                zaccount.logo = l
                zaccount.save()


        if User.objects.filter(username=root.user['username']).count()==0:
            u = User.objects.create_user(root.user['username'], \
                                        root.user['email'], \
                                        root.user['password'])
            u.is_superuser = True
            u.is_staff = True
            u.save()
            zu = ZUser(user=u)
            zu.account = zaccount
            zu.is_admin = True
            zu.save()
