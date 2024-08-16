from django import forms
from .models import CarModel


class CarModelViewForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = "__all__"
        widgets = {
            'car_name': forms.Select(attrs={'class': 'form-control'}),
        }


class CarModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = "__all__"
        widgets = {
            'car_name': forms.Select(attrs={'class': 'form-control'}),
            'VIN_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'car_name': 'خودرو',
            'VIN_number': 'شماره شاسی',
        }

    def clean_VIN_number(self):
        VIN_number = self.cleaned_data['VIN_number']
        if VIN_number <= 0:
            raise forms.ValidationError("شماره شاسی باید بیشتر از صفر باشد.")
        return VIN_number


class CarUpdateModelForm(forms.ModelForm):
    class Meta:
        model = CarModel
        fields = "__all__"
        widgets = {
            'car_name': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'car_name': 'خودرو',
            'VIN_number': 'شماره شاسی',
        }


cars = (('', ''), ('T5', 't5'), ('M4', 'm4'), ('SX5', 'sx5'), ('B511', 'B511'),)


class CarsFilterForm(forms.Form):
    car_name = forms.CharField(
        required=False,
        widget=forms.Select(choices=cars, attrs={'class': 'form-control'}),
        label='خودرو'
    )
    VIN_number_from = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='شماره شاسی از'
    )
    VIN_number_to = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='شماره شاسی تا'
    )
