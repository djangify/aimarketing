# contact/admin.py
from django.contrib import admin
from .models import ContactSubmission

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'ip_address', 'service_type', 'created_at', 'is_read', 'is_blocked')
    list_filter = ('service_type', 'used_before', 'is_read', 'is_blocked', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message', 'ip_address')
    readonly_fields = ('ip_address', 'user_agent', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Request Details', {
            'fields': ('service_type', 'used_before', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_blocked')
        }),
        ('Technical Information', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread', 'block_ips', 'unblock_ips']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected submissions as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected submissions as unread"
    
    def block_ips(self, request, queryset):
        queryset.update(is_blocked=True)
    block_ips.short_description = "Block IPs from selected submissions"
    
    def unblock_ips(self, request, queryset):
        queryset.update(is_blocked=False)
    unblock_ips.short_description = "Unblock IPs from selected submissions"