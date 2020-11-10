from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.debug import sensitive_variables

from requests.exceptions import RequestException

from platform_apis.models import DeezerOAuthError
from deezerdata.models.deezer_account import DeezerAccount

from .models import Profile

class DisplayProfile(LoginRequiredMixin, View):
    """
    Displays the profile of the current user.
    """
    def get(self, request):
        profile = request.user.profile
        platform_accounts = profile.platformaccount_set.all()
        deezer_accounts = []
        for account in platform_accounts:
            try:
                deezer_accounts.append(account.deezeraccount)
            except AttributeError:  # This account is not a DeezerAccount
                pass

        deezer_link_account_url = settings.DEEZER_OAUTH_URL.format(
            settings.DEEZER_API_APP_ID, settings.DEEZER_AUTH_REDIRECT_URI
        )
        return render(request, "accounts/display_profile.html", locals())


class GetDeezerOAuthCode(View, LoginRequiredMixin):
    """
    View linked to the url to which the user is redirected after
    authorizing acces to his account on Deezer.
    """
    @sensitive_variables('access_token', 'code')
    def get(self, request):
        profile = request.user.profile
        try:
            if "code" in request.GET:
                code = request.GET["code"]
                access_token = profile.get_deezer_access_token(code)
                try:
                    profile.add_deezer_account(access_token)
                    messages.success(
                        request,
                        "Votre compte Deezer a été lié à votre "
                        "profil MuzHistory.",
                    )
                except ValueError:
                    messages.error(
                        request,
                        "Ce compte Deezer est déjà lié à un autre profile MuzHistory.",
                    )
            elif "error_reason" in request.GET:
                if request.GET["error_reason"] == "user_denied":
                    messages.error(
                        request,
                        "Vous avez refusé l'accès à votre "
                        "compte Deezer. Celui-ci n'a pas été lié à "
                        "MuzHistory.",
                    )
                else:
                    raise DeezerOAuthError(request.GET["error_reason"])
            else:
                raise DeezerOAuthError("Unknown error.")

        except (RequestException, DeezerOAuthError) as error:
            messages.error(
                request,
                "Nous avons rencontré un problème lors "
                "de la connexion à Deezer. Votre compte Deezer n'a pas "
                "pu être lié.",
            )

        return redirect("accounts:display-profile")
