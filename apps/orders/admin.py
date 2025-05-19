from django.contrib import admin
from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        ("General Info", {"fields": ("order_number", "customer", "date_time_edited", "status", "description")}),
        ("Order Items", {"fields": ()}),
    )
    list_display = ("customer", "status", "date_time_edited",)
    search_fields = ("customer", "status", "date_time_edited", "description",)
    list_filter = ("status",)

    def order_number(self, obj):
        return obj.id

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return ['order_number', 'description', 'customer', 'date_time_edited']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)