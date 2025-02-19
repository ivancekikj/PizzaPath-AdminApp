from django.contrib import admin

from apps.accounts.models import Customer, CouponReward, NewsletterPost, WorkingDay

admin.site.register(Customer)
admin.site.register(CouponReward)
admin.site.register(NewsletterPost)
admin.site.register(WorkingDay)