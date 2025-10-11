from django.contrib import admin

from apps.accounts.email_sender import send_newsletter_posts
from apps.accounts.models import CouponReward, Customer, NewsletterPost, User
from project import settings


class EmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ("date_joined", "last_login")
    list_display = ("username", "email", "first_name", "last_name", "is_superuser")
    list_filter = ("is_superuser", "is_active", "is_email_confirmed", "groups")
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    def get_fieldsets(self, request, obj=None):
        return (
            (
                "Account Info",
                {
                    "fields": ("username", "email", "is_email_confirmed", "is_active", "date_joined", "last_login")
                    + (("password",) if obj is None else ())
                },
            ),
            ("Personal Info", {"fields": ("first_name", "last_name")}),
            ("Privileges", {"fields": ("is_superuser", "groups", "user_permissions")}),
        )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        obj.save()


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
    list_filter = ("is_subscribed_to_newsletter", "is_email_confirmed")
    search_fields = ("username", "email", "first_name", "last_name", "address", "phone_number")
    readonly_fields = ("date_joined", "last_login", "coupons", "is_email_confirmed")

    def get_fieldsets(self, request, obj=None):
        return (
            (
                "Account Info",
                {
                    "fields": (
                        "username",
                        "email",
                        "is_email_confirmed",
                        "date_joined",
                        "last_login",
                    )
                    + (("password",) if settings.DEBUG and obj is None else ())
                },
            ),
            ("Personal Info", {"fields": ("first_name", "last_name", "address", "phone_number")}),
            ("Rewards", {"fields": ("coupons",)}),
            ("Newsletter", {"fields": ("is_subscribed_to_newsletter",)}),
        )

    def coupons(self, obj):
        result = ""
        for coupon in CouponReward.objects.filter(customer_id=obj.id):
            result += f"{coupon.food_portion} - {coupon.count}\n"
        return result

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=False)

    def has_add_permission(self, request):
        return settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class NewsletterPostAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    search_fields = ("title", "date")

    def save_model(self, request, obj, form, change):
        obj.save()
        emails = list()
        for customer in Customer.objects.filter(is_subscribed_to_newsletter=True, is_active=True):
            if customer.is_email_confirmed:
                emails.append(customer.email)
            customer.received_posts.add(obj)
            customer.save()
        if len(emails) > 0:
            send_newsletter_posts(emails, obj.title, obj.content)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(User, EmployeeAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(NewsletterPost, NewsletterPostAdmin)
