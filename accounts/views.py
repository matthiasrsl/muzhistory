from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from django.conf import settings

@login_required
def display_profile(request):
    profile = request.user.profile
    deezer_accounts = profile.deezeraccount_set.all()
    deezer_link_account_url = settings.DEEZER_OAUTH_URL.format(
            settings.DEEZER_API_APP_ID, 
            settings.DEEZER_AUTH_REDIRECT_URI
    )
    return render(request, 'accounts/display_profile.html', locals())
    
    
class GetDeezerOAuthCode(View, LoginRequiredMixin):
    """
    View linked to the url to which the user is redirected after
    authorizing acces to his account on Deezer.
    """
    def get(self, request):
        code = request.GET['code']
        profile = request.user.profile 
        
        access_token = profile.get_deezer_access_token(code)
        profile.add_deezer_account(access_token)
        
        return redirect(display_profile)
