# apps/prompts/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Prompt


# --- List all prompts or filter by category ---
def prompt_list(request):
    category = request.GET.get("category")
    if category:
        prompts = Prompt.objects.filter(category=category)
    else:
        prompts = Prompt.objects.all()
    return render(
        request,
        "prompts/prompt_list.html",
        {"prompts": prompts, "selected_category": category},
    )


# --- View single prompt ---
def prompt_detail(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk)
    return render(request, "prompts/prompt_detail.html", {"prompt": prompt})


# --- Toggle save/unsave favourite prompt ---
@login_required
def toggle_favourite_prompt(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "error": "Invalid request method."}, status=400
        )

    prompt_id = request.POST.get("prompt_id")
    if not prompt_id:
        return JsonResponse(
            {"success": False, "error": "Missing prompt ID."}, status=400
        )

    prompt = get_object_or_404(Prompt, id=prompt_id)
    profile = request.user.profile  # assumes OneToOne relationship

    if prompt in profile.saved_prompts.all():
        profile.saved_prompts.remove(prompt)
        is_saved = False
    else:
        profile.saved_prompts.add(prompt)
        is_saved = True

    return JsonResponse({"success": True, "is_saved": is_saved})


# --- Dashboard view of saved prompts ---
@login_required
def dashboard_saved_prompts(request):
    profile = request.user.profile
    saved = profile.saved_prompts.all()
    return render(
        request, "prompts/dashboard_saved_prompts.html", {"saved_prompts": saved}
    )
