import re


def format_phone_number(phone):
    phone_number = re.sub(r'[^\d+]', '', phone)

    if phone_number.startswith('8') or phone_number.startswith('7'):
        phone_number = '+7' + phone_number[1:]
    elif phone_number.startswith('9'):
        phone_number = '+7' + phone_number

    return phone_number


def get_site_url():
    from django.contrib.sites.models import Site

    scheme = "https"
    domain = Site.objects.get_current().domain
    return "{}://{}".format(scheme, domain)
