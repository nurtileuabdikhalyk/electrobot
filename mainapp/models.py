from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField('Категория аты', max_length=250)
    slug = models.SlugField('Слаг')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категориялар'


class Product(models.Model):
    name = models.CharField('Өнім аты', max_length=250)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    price = models.DecimalField('Бағасы', max_digits=9, decimal_places=2)
    image = models.ImageField('Сурет', upload_to='product_image/')
    description = models.TextField('Сипаттама')
    created = models.DateTimeField('Уақыты', auto_now_add=True)
    slug = models.SlugField('Слаг')

    def __str__(self):
        return f"{self.name} {self.category.name}"

    class Meta:
        verbose_name = 'Өнім'
        verbose_name_plural = 'Өнімдер'


class Customer(models.Model):
    user = models.OneToOneField(User, verbose_name='Қолданушы', on_delete=models.CASCADE)
    first_name = models.CharField('Есімі', max_length=150)
    last_name = models.CharField('Тегі', max_length=150, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=16)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Қолданушы'
        verbose_name_plural = 'Қолданушы'


class ProductImages(models.Model):
    product = models.ForeignKey(Product, verbose_name='Өнім', on_delete=models.CASCADE)
    image = models.ImageField('Сурет', upload_to='product_images/')

    def __str__(self):
        return f"{self.product.name}"

    class Meta:
        verbose_name = 'Сурет'
        verbose_name_plural = 'Суреттер'


class Order(models.Model):
    product = models.ForeignKey(Product, verbose_name='Өнім', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, verbose_name='Қолданушы', on_delete=models.CASCADE)
    quantity = models.IntegerField('Саны', default=1)
    price = models.DecimalField('Сумма', max_digits=15, decimal_places=2)
    city = models.CharField('Қала', max_length=150)
    street = models.CharField('Көше', max_length=150)
    house = models.IntegerField('Үй')
    house_number = models.IntegerField('Үй номері')
    oplata = models.CharField('Төлем түрі', max_length=30)
    date = models.DateTimeField('Уақыты', auto_now_add=True)
    status = models.BooleanField('Орындалды ма?', default=False)

    def __str__(self):
        return f"{self.customer.first_name} {self.product.name}"

    class Meta:
        verbose_name = 'Тапсырыс'
        verbose_name_plural = 'Тапсырыстар'


class Contact(models.Model):
    first_name = models.CharField('Есімі', max_length=150)
    last_name = models.CharField('Тегі', max_length=150, blank=True, null=True)
    message = models.TextField('Хабарлама')
    created = models.DateTimeField('Уақыты', auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Байланыс'
        verbose_name_plural = 'Байланыстар'
