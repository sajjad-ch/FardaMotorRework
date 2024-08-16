from django.db import models

# Create your models here.

cars = (('T5', 't5'), ('M4', 'm4'), ('SX5', 'sx5'), ('B511', 'B511'),)


class CarModel(models.Model):
    car_name = models.CharField(choices=cars, default='T5', verbose_name='نام ماشین', max_length=20)
    VIN_number = models.IntegerField(verbose_name='شماره VIN')

    class Meta:
        verbose_name = 'خودرو'
        verbose_name_plural = 'خودرو ها'

    def __str__(self):
        return f"{self.car_name} - {str(self.VIN_number)}"
