from django.conf import settings

def recaptcha_context(request):
    return {
        'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY
    }
