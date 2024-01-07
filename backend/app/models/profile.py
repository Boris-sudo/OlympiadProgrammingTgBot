from django.db import models
from django.contrib.auth.models import User


class Bot(models.Model):
    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    class Variants(models.IntegerChoices):
        REALTOR = 0, "Риелтор"
        GPT = 1, "GPT-бот"
        OTHER = 3, "Другой"

    variant = models.IntegerField(choices=Variants.choices, verbose_name="Тип")

    session_string = models.CharField(max_length=1000, null=True, verbose_name="Строка сессии")
    user_id = models.BigIntegerField(unique=True, null=True, editable=False, verbose_name="Id пользователя")
    proxy = models.OneToOneField(Proxy, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Прокси")

    enabled = models.BooleanField(blank=True, default=True, verbose_name="Включен ли")
    flood = models.BooleanField(blank=True, default=False, verbose_name="Блокировка флуд")

    app_version = models.TextField(blank=True, null=True)
    device_model = models.TextField(blank=True, null=True)
    system_version = models.TextField(blank=True, null=True)
    lang_code = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_variant_display()} №{self.id}"

    def save(self, *args, **kwargs):
        api = API.TelegramDesktop.Generate()
        if not self.app_version:
            self.app_version = api.app_version
        if not self.device_model:
            self.device_model = api.device_model
        if not self.system_version:
            self.system_version = api.system_version
        if not self.lang_code:
            self.lang_code = api.lang_code
        return super().save(*args, **kwargs)

    def _get_client(self, proxy: typing.Optional[Proxy] = None) -> typing.Optional[PyrogramClient]:
        if self.session_string:
            client = getattr(self, "_client", None)
            if not client:
                client = PyrogramClient(
                    str(self), session_string=self.session_string, proxy=proxy.as_dict() if proxy and proxy.working else None,
                    app_version=self.app_version, device_model=self.device_model,
                    system_version=self.system_version, lang_code=self.lang_code
                )
                setattr(self, "_client", client)
            return client

    @property
    def client(self) -> typing.Optional[PyrogramClient]:
        return self._get_client(self.proxy)

    async def aclient(self) -> typing.Optional[PyrogramClient]:
        proxy = await sync_to_async(lambda: self.proxy)()
        return self._get_client(proxy)


class AbstractSettings(models.Model):
    class Meta:
        verbose_name = "Настройки бота"
        verbose_name_plural = "Настройки бота"
        abstract = True

    bot = models.OneToOneField(Bot, on_delete=models.CASCADE, verbose_name="Бот")


class Proxy(models.Model):
    class Schemes(models.TextChoices):
        SOCKS5 = "socks5"
        SOCKS4 = "socks4"
        HTTP = "http"

    scheme = models.CharField(choices=Schemes.choices, default=Schemes.SOCKS5, max_length=6, verbose_name="Тип")
    hostname = models.CharField(max_length=50, verbose_name="Имя хоста")
    port = models.PositiveIntegerField(blank=True, verbose_name="Порт")

    username = models.CharField(max_length=50, blank=True, verbose_name="Логин")
    password = models.CharField(max_length=50, blank=True, verbose_name="Пароль")

    rating = models.IntegerField(default=1000, blank=True, verbose_name='Рейтинг')
