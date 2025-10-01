# contact/forms.py
from django import forms
from .models import ContactSubmission
import re

class ContactForm(forms.Form):
    BLOCKED_DOMAINS = [
        'gmail.com',
        'hotmail.com',
        'outlook.com',
        'yahoo.com',
        'proton.me',
        'protonmail.com',
        'aol.com',
        'icloud.com',
        'mail.com',
        'zoho.com',
        'yandex.com',
        'gmx.com',
        'live.com',
        'msn.com',
    ]
    
    name = forms.CharField(required=True)
    email = forms.EmailField(
        required=True,
        help_text="Please use your business email. Personal email domains (Gmail, Hotmail, etc.) are not accepted."
    )
    phone = forms.CharField(required=False)
    service_type = forms.ChoiceField(choices=ContactSubmission.SERVICE_CHOICES, required=True)
    used_before = forms.ChoiceField(choices=ContactSubmission.USED_BEFORE_CHOICES, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
 
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            domain = email.split('@')[-1].lower()
            if domain in self.BLOCKED_DOMAINS:
                raise forms.ValidationError(
                    "ERROR: Business email required. Personal emails like Gmail, Hotmail, etc. are not accepted."
                )
        return email
    