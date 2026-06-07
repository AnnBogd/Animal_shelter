"""Модели приложения animals."""

from dateutil.relativedelta import relativedelta
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Animal(models.Model):
    """Модель животного."""

    ANIMAL_CHOICES = [
        ('cat', 'Кошка'),
        ('dog', 'Собака'),
        ('bird', 'Птица'),
        ('rodent', 'Грызун'),
        ('insect', 'Насекомое'),
        ('reptile', 'Рептилия / Земноводное'),
        ('fish', 'Рыба'),
        ('exotic', 'Экзотическое животное'),
        ('farm', 'Сельскохозяйственное'),
        ('other', 'Другое'),
    ]
    GENDER_CHOICES = [
        ('male', 'Самец'),
        ('female', 'Самка'),
    ]
    STATUS_CHOICES = [
        ('shelter', 'В приюте'),
        ('adopted', 'Забрали домой'),
    ]
    name = models.CharField(verbose_name='Кличка', max_length=100)
    species = models.CharField(
        max_length=20,
        choices=ANIMAL_CHOICES,
        verbose_name='Вид животного'
    )
    breed = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Порода',
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name='Пол животного',
    )
    birth_date = models.DateField(verbose_name='Дата рождения')
    arrival_date = models.DateField(verbose_name='Дата поступления в приют')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='shelter',
        verbose_name='Статус',
    )
    adoption_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата отъезда домой',
    )
    bio = models.TextField(verbose_name='Биография')
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='animals/',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL',
        blank=True,
    )

    class Meta:
        verbose_name = 'животное'
        verbose_name_plural = 'животные'

    def _declension(self, age, one, two, five):
        """Подобрать склонение для возраста животного.

        Пример: _declension(3, 'год', 'года', 'лет') → 'года'.
        """
        if 11 <= age % 100 <= 19:
            return five
        if age % 10 == 1:
            return one
        if 2 <= age % 10 <= 4:
            return two
        return five

    @property
    def age(self) -> int:
        """Вернуть возраст животного на данный момент."""
        if not self.birth_date:
            return "возраст неизвестен"
        age = relativedelta(timezone.now().date(), self.birth_date)
        if age.years >= 1:
            return (f'{age.years} '
                    f'{self._declension(age.years, 'год', 'года', 'лет')}')
        elif age.months >= 1:
            return (f'{age.months} '
                    f'{self._declension(
                        age.months, 'месяц', 'месяца', 'месяцев')}')
        elif age.days >= 1:
            return (f'{age.days} '
                    f'{self._declension(age.days, 'день', 'дня', 'дней')}')
        else:
            return "новорожденный"

    def save(self, *args, **kwargs) -> None:
        """Сформировать слаг из имени с номером при дублировании."""
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Animal.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Вернуть URL объекта."""
        return reverse('animal_detail', kwargs={'slug': self.slug})

    def __str__(self) -> str:
        """Переопределить строковое представление объекта."""
        return f'{self.name} ({self.species})'


class AdoptionRequest(models.Model):
    """Модель заявки на знакомство с животным."""

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='requests',
        verbose_name='Желаемое животное',
    )
    name = models.CharField(verbose_name='Имя посетителя')
    phone = models.CharField(verbose_name='Телефон посетителя')
    email = models.EmailField(
        verbose_name='Электронная почта посетителя',
        blank=True,
        null=True,
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания заявки',
        auto_now_add=True,
    )
    is_processed = models.BooleanField(
        verbose_name='Статус обработки заявки',
        default=False,
    )
