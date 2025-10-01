from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ContactSubmission
from .forms import ContactForm
import ipaddress


def get_client_ip(request):
    """Extract client IP from headers or remote address."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def contact_view(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST":
        # Check for personal email domains before form validation
        email = request.POST.get("email", "")
        if email:
            domain = email.split("@")[-1].lower()
            blocked_domains = [
                "gmail.com",
                "hotmail.com",
                "outlook.com",
                "yahoo.com",
                "proton.me",
                "protonmail.com",
                "aol.com",
                "icloud.com",
                "mail.com",
                "zoho.com",
                "yandex.com",
                "gmx.com",
                "live.com",
                "msn.com",
            ]
            if domain in blocked_domains:
                return render(request, "contact/email_error.html", {"email": email})

        # If email domain check passes, continue with normal form validation
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data.get("phone", "")
            service_type = form.cleaned_data["service_type"]
            used_before = form.cleaned_data["used_before"]
            message = form.cleaned_data["message"]

            # Get IP address and user agent
            raw_ip = get_client_ip(request)
            user_agent = request.META.get("HTTP_USER_AGENT", "")

            # Convert raw string to proper IP object
            ip_obj = None
            if raw_ip:
                try:
                    ip_obj = ipaddress.ip_address(raw_ip)
                except ValueError:
                    ip_obj = None  # invalid IP, ignore

            # Check if IP is blocked
            if (
                ip_obj
                and ContactSubmission.objects.filter(
                    ip_address=ip_obj, is_blocked=True
                ).exists()
            ):
                # Silently fail without letting the user know they're blocked
                return redirect("contact:thanks", submission_id=1)

            # Save to database with IP address
            submission = ContactSubmission.objects.create(
                name=name,
                email=email,
                phone=phone,
                service_type=service_type,
                used_before=used_before,
                message=message,
                ip_address=ip_obj,
                user_agent=user_agent,
            )

            # Send email notification (placeholder for future use)
            try:
                pass
            except Exception as e:
                print(f"Email sending error: {str(e)}")

            return redirect("contact:thanks", submission_id=submission.id)
        else:
            messages.error(request, "Please correct the errors in the form.")

    return render(request, "contact/contact.html", {"form": form})


def thanks_view(request, submission_id):
    submission = get_object_or_404(ContactSubmission, id=submission_id)
    return render(request, "contact/thanks.html", {"submission": submission})


def email_error_view(request):
    return render(request, "contact/email_error.html")
