from django.core.exceptions import ValidationError


def valid_number(value):
    if value[0] == '+':
        raise ValidationError("Укажите номер без +")


def valid_number_2(value):
    if not value.isdigit():
        raise ValidationError("Введите только цифры.")
