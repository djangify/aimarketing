from django.shortcuts import render, redirect
from contact.forms import ContactForm
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.urls import reverse
from news.models import Post, Category
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib import messages
from .forms import SupportForm


def home(request):
    form = ContactForm()
    return render(request, "core/home.html", {"form": form})


def about(request):
    form = ContactForm()
    return render(request, "core/about.html", {"form": form})


def policies_index_view(request):
    """View function for the policies index page."""
    breadcrumbs = [{"title": "Policies", "url": None}]
    template_name = "core/policy/policies_index.html"
    return render(request, template_name, {"breadcrumbs": breadcrumbs})


def privacy_view(request):
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Privacy Policy", "url": None},
    ]
    template_name = "core/policy/privacy.html"
    return render(request, template_name, {"breadcrumbs": breadcrumbs})


def cookie_view(request):
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Cookie Policy", "url": None},
    ]
    template_name = "core/policy/cookies.html"
    return render(request, template_name, {"breadcrumbs": breadcrumbs})


def affiliate_view(request):
    breadcrumbs = [
        {"title": "Affiliate", "url": reverse("core:policies_index")},
        {"title": "Affiliate Policy", "url": None},
    ]
    template_name = "core/policy/affiliate.html"
    return render(request, template_name, {"breadcrumbs": breadcrumbs})


def terms_view(request):
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Terms & Conditions", "url": None},
    ]
    template_name = "core/policy/terms.html"
    return render(request, template_name, {"breadcrumbs": breadcrumbs})


def ai_writing_view(request):
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "AI Writing Policy", "url": None},
    ]
    template_name = "core/policy/ai-writing-policy.html"
    return render(request, template_name, {"breadcrumbs": breadcrumbs})


def support_view(request):
    breadcrumbs = [
        {"title": "Policies", "url": reverse("core:policies_index")},
        {"title": "Support Policy", "url": None},
    ]
    template_name = "core/policy/support.html"
    return render(request, template_name, {"breadcrumbs": breadcrumbs})


def handler500(request):
    return render(request, "error/500.html", status=500)


def handler403(request, exception):
    return render(request, "error/403.html", status=403)


def handler404(request, exception):
    # Define which category to show (by slug)
    category_slug = "tech-va"  # Change this to your desired category slug

    try:
        # Try to get the category
        category = get_object_or_404(Category, slug=category_slug)

        # Get posts from the category
        category_posts = Post.objects.filter(
            category=category, status="published", publish_date__lte=timezone.now()
        ).order_by("-publish_date")[:4]

    except Http404:
        # Fallback to recent posts if category doesn't exist
        category_posts = Post.objects.filter(
            status="published", publish_date__lte=timezone.now()
        ).order_by("-publish_date")[:3]
        category = None

    context = {"category_posts": category_posts, "selected_category": category}

    return render(request, "error/404.html", context, status=404)


@require_GET
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def support(request):
    form = SupportForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()  # saves to DB + emails + auto-ack
        messages.success(request, "Thank you! Your message has been sent.")
        return redirect("core:support")
    return render(request, "core/support.html", {"form": form})
