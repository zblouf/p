def post_login(request, user, account):
    # ToDo : setting the current Entity
    request.session['account_id'] = account.id
