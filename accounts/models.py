# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import uuid
from datetime import timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    verified = models.BooleanField(default=False)
    bio = models.TextField(max_length=650, blank=True)

    # --- Business information (from promptsite) ---
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_type = models.CharField(max_length=255, blank=True, null=True)
    business_location = models.CharField(max_length=255, blank=True, null=True)
    target_audience = models.CharField(max_length=255, blank=True, null=True)

    # --- E-commerce favourites (from aimarketing) ---
    favourite_products = models.ManyToManyField(
        "shop.Product", blank=True, related_name="favorited_by"
    )

    # --- Promptsite fields ---
    saved_prompts = models.ManyToManyField(
        "prompts.Prompt", blank=True, related_name="saved_by"
    )
    saved_templates = models.ManyToManyField(
        "prompt_templates.PromptTemplate", blank=True, related_name="saved_by"
    )

    def __str__(self):
        return f"{self.user.username}'s profile"


# --- Profile creation signals ---
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except User.profile.RelatedObjectDoesNotExist:
        UserProfile.objects.create(user=instance)


# --- Email Verification Token ---
class EmailVerificationToken(models.Model):
    """Model for email verification tokens"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_sent = models.BooleanField(default=False)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)

    def is_valid(self):
        # Token expires after 24 hours
        return self.created_at >= timezone.now() - timedelta(hours=24)

    def __str__(self):
        return f"Verification for {self.user.username}"


# --- Member Resources (from main site) ---
class MemberResource(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to="member_resources/")
    thumbnail = models.ImageField(upload_to="member_resources/thumbnails/")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title
