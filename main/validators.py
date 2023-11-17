from django.core.exceptions import ValidationError

def validate_non_negative(value):
    if value < 1:
        raise ValidationError("Число не может быть отрицательным или = 0 .")
    
def min_sum(value):
    if value < 50:
        raise ValidationError("Минимальная сумма подписки 50 руб.")