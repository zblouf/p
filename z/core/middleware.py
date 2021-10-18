from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User, AnonymousUser
#from z.core.app.models import App, AppRegistration
from time import time
from z.org.entity.models import Entity
#from z.saas.models import Account
from django.conf import settings
import logging

logger = logging.getLogger('p')

class ZMiddleware(object):
    def process_request(self, request):
        request.settings = settings
        request.account = None
        request.activity = None
        request.entity = None
        request.zuser = None
        request.authorized_entities = []
        request.authorized_apps = []

        return None

class ACLMiddleware(object):
    def process_request(self, request):
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "This ACL middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")

        ae = []
        if hasattr(request, 'user') and not isinstance(request.user, AnonymousUser):
            u = request.user
            try:
                zu = u.zuser
            except:
                logger.warning("[ACL Middleware] ZUser affectation failed.")
            request.zuser = zu
            if zu.is_admin:
                ae = Entity.objects.filter(account=zu.account)
                logger.info('  -> user is a customer admin, setting authorized_entities to %s', repr(ae))
        request.authorized_ent = ae
        return None

class TimerMiddleware:
    def process_request(self, request):
        request._tm_start_time = time()

    def process_response(self, request, response):
        if not hasattr(request, "_tm_start_time"):
            return response
        total = time() - request._tm_start_time
        logger.info("Processing time : %fs" %(total))
        return response
