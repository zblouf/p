from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.conf import settings

def index(request):
    return HttpResponseRedirect('/auth/login')

def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect('/auth/login')

def login(request):
    _debug = ""
    from z.auth.zuser.models import LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            from z.saas.models import Account
            from django.contrib.auth.models import User
            from django.contrib.auth import authenticate, login
            from z.core import zutils
            acount = Account.objects.filter(login=form.cleaned_data['account']).count()
            if acount==1:
                a = Account.objects.get(login=form.cleaned_data['account'])
                full_username = zutils.full_username(form.cleaned_data['username'], a)
                u = authenticate(username=full_username, password=form.cleaned_data['password'])
                if u is not None:
                    if u.is_active:
                        login(request, u)
                        # post-login operations
                        from z.auth import login_utils
                        login_utils.post_login(request, u, a)
                        return redirect('/home')
                    else:
                        _debug += "account disabled. "
                        # user account has been disabled
                else:
                        _debug += "authentification failed (%s:%s). " %(form.cleaned_data['username'], form.cleaned_data['password'])
                    # authentification failed
            elif acount==0:
                _debug += "unknown customer account : %s. " %(form.cleaned_data['account'])
            else:
                _debug += "%d customer accounts share the same id (%s). " %(ccount, form.cleaned_data['account'])
                # more than a unique customer with given login. shouldn't append
                # since model has a unique constraint.
    else:
        form = LoginForm() # An unbound form

    return render_to_response('auth/login.html', {
        'form': form, 'debug': _debug
    }, context_instance=RequestContext(request))


def lost_password(request, email_errors=[]):
    from z.auth.zuser.models import LostPasswordForm
    from z.auth.zuser.models import ZUser
    from django.contrib.auth.models import User
    if request.method == 'POST':
        form = LostPasswordForm(request.POST)
        if form.is_valid():
            ucount = User.objects.filter(email=form.cleaned_data['email']).count()
            if ucount==1:
                # unique email in users
                u = User.objects.filter(email=form.cleaned_data['email'])[0]
                from django.core.mail import send_mail
                send_mail(  '[Générisque] perte/oubli mot de passe', 
                            'Bonjour %s %s,\n\n votre nouveau mot de passe est : %s' %(
                            u.first_name, u.last_name, "todo"), 
                            'support@generisque.net',
                            [u.email], fail_silently=False)

                return HttpResponseRedirect('/auth/reset_password/') # Redirect after POST
            elif ucount==0:
                email_errors.append("Aucun utilisateur ne correspond à cette adresse mail.")
                return redirect('lost_password', email_errors=email_errors)
                # no user found matching email
            else:
                # multiple users share the same email
                return redirect('lost_password', email_errors=email_errors)

            return HttpResponseRedirect('/auth/reset_password/') # Redirect after POST
    else:
        form = LostPasswordForm() # An unbound form
    return render_to_response('auth/lost_password.html', {
        'form': form, 'settings': settings, 'email_errors': email_errors
    }, context_instance=RequestContext(request))

def reset_password(request):
    return render_to_response('auth/reset_password.html', {
        'settings': settings, 
    }, context_instance=RequestContext(request))
