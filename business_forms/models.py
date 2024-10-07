import os
import re

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import SuspiciousFileOperation
from django.db import models
from django.utils.html import format_html
from business_forms.utils import format_phone_number
from multiselectfield import MultiSelectField


def safe_filename(filename):
    filename = re.sub(r'[^\w\s.-]', '', filename).strip()
    if '..' in filename or filename.startswith('/'):
        raise SuspiciousFileOperation("Detected path traversal attempt")
    return filename


class BusinessForm(models.Model):
    def get_upload_photo_path(self, filename):
        filename = safe_filename(filename)
        return os.path.join('banners', filename)

    def get_upload_spasibo_path(self, filename):
        filename = safe_filename(filename)
        return os.path.join('spasibo', filename)

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    photo = models.ImageField(upload_to=get_upload_photo_path)
    spasibo_photo = models.ImageField(upload_to=get_upload_spasibo_path)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Конфигурации форм"
        verbose_name_plural = "Конфигурации форм"


class BaseModelForm:

    @property
    def instagram_link(self):
        return f"https://instagram.com/{self.instagram_username}"

    @property
    def tg_username_link(self):
        tg_username = self.tg_username.replace("@", '')
        return f"https://t.me/{tg_username}"

    @property
    def tg_phone_link(self):
        return f"https://t.me/{format_phone_number(self.phone)}"

    def formatted_instagram_link(self):
        return format_html("<a href=\"{}\" target=\"_blank\">{}</a>", self.instagram_link, 'Посмотреть Instagram')

    def formatted_tg_username_link(self):
        return format_html("<a href=\"{}\" target=\"_blank\">{}</a>", self.tg_username_link, 'Написать человеку')

    def formatted_tg_phone_link(self):
        return format_html("<a href=\"{}\" target=\"_blank\">{}</a>", self.tg_phone_link, 'Написать человеку')

    formatted_instagram_link.short_description = 'Ссылка на instagram'
    formatted_tg_username_link.short_description = 'Ссылка TG сформированная по никнейму'
    formatted_tg_phone_link.short_description = 'Ссылка TG сформированная по номеру телефона'


class UltimaRequest(models.Model, BaseModelForm):
    STATUS_CHOICES = (
        (1, "Открыт"),
        (2, "Связался, жду ответ"),
        (3, "Не отвечает"),
        (4, "Закрыто"),
    )

    CURRENCY_CHOICES = (
        ('rub', 'Рубли'),
        ('usd', 'Доллары США'),
        ('eur', 'Евро'),
        ('cny', 'Юани'),
        ('aed', 'Дирхамы'),
        ('other', 'Другая валюта'),
    )

    AGE_CHOICES = (
        ('under_23', 'До 23 лет'),
        ('24_40', 'От 24 до 40 лет'),
        ('41_60', 'От 41 до 60 лет'),
        ('over_60', 'Старше 60 лет'),
    )

    INVESTMENT_GOAL_CHOICES = (
        ('inflation_protection', 'Защита средств от инфляции'),
        ('pension', 'Прибавка к пенсии'),
        ('additional_income', 'Получение дополнительного дохода'),
        ('children_future', 'На будущее детей'),
        ('other', 'Другая причина'),
    )

    INVESTMENT_PERIOD_CHOICES = (
        ('less_than_3', 'Менее 3 лет'),
        ('3_to_5', 'От 3 до 5 лет'),
        ('5_to_10', 'От 5 до 10 лет'),
        ('more_than_10', 'Свыше 10 лет'),
    )

    SAVINGS_CHOICES = (
        ('10_30', 'От 10 до 30 млн. рублей'),
        ('30_100', 'От 30 до 100 млн. рублей'),
        ('over_100', 'Свыше 100 млн. рублей'),
    )

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Отметка времени", null=True, blank=True)
    name = models.CharField(
        max_length=255, verbose_name="ФИО",
        null=True, blank=True
    )

    phone = models.CharField(
        max_length=20, verbose_name="Номер телефона",
        null=True, blank=True
    )

    city = models.CharField(
        max_length=255, verbose_name="Город проживания",
        null=True, blank=True
    )

    currency = MultiSelectField(
        choices=CURRENCY_CHOICES,
        max_length=255,
        verbose_name="Укажите валюту инвестирования (можно отметить несколько вариантов):",
        null=True, blank=True
    )

    age = models.CharField(
        max_length=255, choices=AGE_CHOICES,
        verbose_name="Укажите информацию о Вашем возрасте:",
        null=True, blank=True
    )

    investment_goal = models.CharField(
        max_length=255, choices=INVESTMENT_GOAL_CHOICES,
        verbose_name="Укажите Вашу цель инвестирования (пожалуйста, отметьте один вариант)",
        null=True, blank=True
    )

    investment_period = models.CharField(
        max_length=255, choices=INVESTMENT_PERIOD_CHOICES,
        verbose_name="Укажите срок инвестирования ",
        null=True, blank=True
    )

    available_sum = models.CharField(
        max_length=255, choices=SAVINGS_CHOICES,
        verbose_name="Укажите информацию о наличии и сумме Ваших сбережений",
        null=True, blank=True
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    policy_agreement = models.BooleanField(
        verbose_name="Согласен с политикой обработки персональных данных",
        default=False
    )
    additional_question = models.TextField(verbose_name="Для дополнительных вопросов:", null=True, blank=True)
    description = models.TextField(verbose_name="Комментарий менеджера", null=True, blank=True)

    def colored_status(self):
        color = 'black'
        background_color = 'white'
        if self.status == 2:
            color = 'white'
            background_color = '#4dab4d'
        elif self.status == 3:
            color = 'white'
            background_color = '#ff9c00'
        elif self.status == 4:
            color = 'white'
            background_color = '#ff0000'
        elif self.status == 5:
            color = 'white'
            background_color = 'black'
        return format_html(
            '<span style="background-color: {}; color: {}; border: 1px solid black; position:relative; display: '
            'block; padding: 5px; text-align: center;'
            'margin: -5px; border-radius: 8px;">{}</span>', background_color, color,
            self.get_status_display()
        )

    colored_status.short_description = 'Статус'

    def __str__(self):
        return f"Анкета записи: {self.name}"

    class Meta:
        verbose_name = "запись в анкете"
        verbose_name_plural = "Анкета записи"
