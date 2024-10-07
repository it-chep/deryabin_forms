from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group

from business_forms.models import UltimaRequest, BusinessForm


class UltimaRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'timestamp', 'colored_status', 'name',
        'phone', 'city', 'currency', 'age',
        'investment_goal', 'investment_period', 'available_sum',
    )

    list_filter = (
        'status', 'timestamp',
        'currency', 'age', 'investment_goal',
        'investment_period', 'available_sum',
    )

    readonly_fields = (
        'name', 'phone', 'city',
        'age', 'investment_goal', 'investment_period',
        'available_sum',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class BusinessFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('content_type',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['content_type'].queryset = ContentType.objects.filter(
            model__in=['ultimarequest'])
        return form


admin.site.register(UltimaRequest, UltimaRequestAdmin)
admin.site.register(BusinessForm, BusinessFormAdmin)

admin.site.unregister(Group)
