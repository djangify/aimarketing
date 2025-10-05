# prompts/urls.py
from django.urls import path
from . import views

app_name = "prompts"

urlpatterns = [
    # List all prompts or filter by category
    path("", views.prompt_list, name="prompt_list"),
    # View single prompt
    path("<int:pk>/", views.prompt_detail, name="prompt_detail"),
    # AJAX: toggle favourite (save/unsave)
    path(
        "toggle-favourite/",
        views.toggle_favourite_prompt,
        name="toggle_favourite_prompt",
    ),
    # Dashboard: saved prompts
    path(
        "dashboard/saved/",
        views.dashboard_saved_prompts,
        name="dashboard_saved_prompts",
    ),
]
