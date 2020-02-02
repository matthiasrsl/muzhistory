from requests.exceptions import RequestException

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from django.conf import settings

from platform_apis.models import DeezerOAuthError


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
        profile = request.user.profile
        
        try:
            if 'code' in request.GET:
                code = request.GET['code']
                access_token = profile.get_deezer_access_token(code)
                profile.add_deezer_account(access_token)
                messages.success(request, "Votre compte Deezer a été lié à votre "
                        "profil MuzHistory."
                )
            elif 'error_reason' in request.GET:
                if request.GET['error_reason'] == 'user_denied':
                    messages.error(request, "Vous avez refusé l'accès à votre "
                            "compte Deezer. Celui-ci n'a pas été lié à "
                            "MuzHistory."
                    )
                else:
                    raise DeezerOAuthError(request.GET['error_reason'])
            else:
                raise DeezerOAuthError("Unknown error.")

        except (RequestException, DeezerOAuthError) as error:
            messages.error(request, "Nous avons rencontré un problème lors "
                    "de la connexion à Deezer. Votre compte Deezer n'a pas "
                    "pu être lié."
            )
            
        return redirect(display_profile)
