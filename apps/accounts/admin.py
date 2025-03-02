from django.contrib import admin
from django.utils import timezone

from apps.accounts.models import Customer, CouponReward, NewsletterPost, WorkingDay, User


class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Account Info", {"fields": ("username", "email", "is_email_confirmed", "is_active", "date_joined", "last_login")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Privileges", {"fields": ("is_superuser", "groups", "user_permissions")}),
    )
    readonly_fields = ("date_joined", "last_login")
    list_display = ("username", "email", "first_name", "last_name", "is_superuser")
    list_filter = ("is_superuser", "is_active", "is_email_confirmed", "groups")
    search_fields = ("username", "email", "first_name", "last_name",)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        obj.save()


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Account Info", {"fields": ("username", "email", "is_email_confirmed", "date_joined", "last_login")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "address", "phone_number")}),
        ("Rewards", {"fields": ("coupons",)}),
        ("Newsletter", {"fields": ("is_subscribed_to_newsletter", "received_posts")}),
    )
    list_display = ("username", "email", "first_name", "last_name",)
    list_filter = ("is_subscribed_to_newsletter", "is_email_confirmed")
    search_fields = ("username", "email", "first_name", "last_name", "address", "phone_number")

    def coupons(self, obj):
        result = ""
        for coupon in CouponReward.objects.filter(customer_id=obj.id):
            result += f"{coupon.food_portion} - {coupon.count}\n"
        return result

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=False)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class NewsletterPostAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    search_fields = ("title", "date")

    def save_model(self, request, obj, form, change):
        obj.save()
        for customer in Customer.objects.filter(is_subscribed_to_newsletter=True):
            customer.received_posts.add(obj)
            customer.save()

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class WorkingDayAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/validate_working_day.js',)

    fieldsets = (
        ("General Info", {"fields": ("date", "is_working_day")}),
        ("Work Time", {"fields": ("start_time", "end_time",)}),
    )
    list_display = ("date", "is_working_day")
    search_fields = ("date", "is_working_day")
    list_filter = ("is_working_day",)

    def has_delete_permission(self, request, obj=None):
        return obj and timezone.now().date() < obj.date

    def has_change_permission(self, request, obj=None):
        return obj and timezone.now().date() < obj.date


admin.site.register(User, EmployeeAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(NewsletterPost, NewsletterPostAdmin)
admin.site.register(WorkingDay, WorkingDayAdmin)
