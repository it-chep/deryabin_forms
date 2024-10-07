import requests
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.conf import settings

from business_forms.forms import UltimaRequestForm
from business_forms.models import BusinessForm, UltimaRequest
from business_forms.utils import format_phone_number, get_site_url


class BaseForm:
    form_method = ""
    client_id = 0

    def call_api_method(self, name, phone_number):
        formatted_phone = format_phone_number(phone_number)
        from business_forms.bot import bot
        message = f"Новая заявка на форму \n\nИмя: {name}\n\nТелефон: {formatted_phone}\n\nДетальная информация находится в админке {get_site_url() + reverse('admin:index')}"
        for admin_id in self.admins:
            bot.send_message(admin_id, message)


class UltimaRequestView(TemplateView, BaseForm):
    template_name = 'business_forms/ultima_form.html'
    form_class = UltimaRequestForm
    form_method = "docstar_push_notification"
    admins = [settings.ADMINS_CHAT_ID]

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(UltimaRequest)
        context["business_form_settings"] = BusinessForm.objects.filter(content_type=content_type).first()
        context["ultima_form"] = self.form_class()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        result = {"success": False}

        if form.is_valid():
            form.save()
            self.call_api_method(form.cleaned_data["name"], form.cleaned_data["phone"])
            result.update({"success": True, "redirect_url": get_site_url() + reverse("spasibo_ultima")})
        else:
            result.update({"errors": form.errors})

        return JsonResponse(result)


class SpasiboUltimaRequestView(TemplateView):
    template_name = 'business_forms/spasibo_ultima_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content_type = ContentType.objects.get_for_model(UltimaRequest)
        context["business_form_settings"] = BusinessForm.objects.filter(content_type=content_type).first()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
