from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import CarModel
from .forms import CarUpdateModelForm, CarModelForm, CarsFilterForm
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Create your views here.


@method_decorator(login_required, name='dispatch')
class CarListView(View):
    def get(self, request):
        car_form = CarsFilterForm()
        cars = CarModel.objects.all().order_by('-id')  # Order by id to get the last 10 cars

        paginator = Paginator(cars, 10)  # Show 10 cars per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'car_form': car_form,
        }
        return render(request, 'car_module/car_list.html', context)


@method_decorator(login_required, name='dispatch')
class CarDetailView(View):
    def get(self, request: HttpRequest, VIN_number, car_name):
        car = get_object_or_404(CarModel, car_name=car_name, VIN_number=VIN_number)
        car_form = CarModelForm(instance=car)
        context = {
            'car_form': car_form
        }
        return render(request, 'car_module/car_detail.html', context)


@method_decorator(login_required, name='dispatch')
class CarUpdateView(View):
    def get(self, request: HttpRequest, VIN_number, car_name):
        car = get_object_or_404(CarModel, car_name=car_name, VIN_number=VIN_number)
        car_form = CarModelForm(instance=car)
        context = {
            'car_form': car_form
        }
        return render(request, 'car_module/car_edit.html', context)

    def post(self, request: HttpRequest, VIN_number, car_name):
        car = get_object_or_404(CarModel, car_name=car_name, VIN_number=VIN_number)
        car_form = CarUpdateModelForm(request.POST, instance=car)
        if car_form.is_valid():
            car_form.save()
            return redirect('car-detail', car_name=car.car_name, VIN_number=car.VIN_number)
        else:
            context = {
                'car_form': car_form,
                'form_errors': car_form.errors,
            }
            return render(request, 'car_module/car_detail.html', context)


@method_decorator(login_required, name='dispatch')
class CarAddView(View):

    def get(self, request):
        car_form = CarModelForm()
        context = {
            'car_form': car_form,
        }
        return render(request, 'car_module/car_add.html', context)

    def post(self, request: HttpRequest):
        car_form = CarModelForm(request.POST)
        if car_form.is_valid():
            print('one')
            VIN_number = car_form.cleaned_data.get('VIN_number')
            car_name = car_form.cleaned_data.get('car_name')
            car = CarModel.objects.filter(car_name__iexact=car_name, VIN_number__exact=VIN_number).first()
            if car is not None:
                print('two')
                car_form.add_error('car_name', 'ماشین با این مشخصات قبلا ثبت شده است.')
                return redirect('car-list')
            else:
                car: CarModel = car_form.save(commit=False)
                car.save()
                return redirect('add-report', car_name=car.car_name, car_VIN=car.VIN_number)

        else:
            context = {
                'car_form': car_form,
            }
            return render(request, 'car_module/car_add.html', context)


@method_decorator(login_required, name='dispatch')
class CarDeleteView(View):
    def get(self, request, VIN_number, car_name):
        car: CarModel = CarModel.objects.filter(car_name__iexact=car_name, VIN_number__exact=VIN_number).first()
        if car:
            car.delete()
            return redirect('car-list')
        else:
            return render(request, 'car_module/car_list.html', context={'error': 'چنین خودرویی وجود ندارد.'})


@method_decorator(login_required, name='dispatch')
class FilterCarView(View):
    def get(self, request):
        car_form = CarsFilterForm()
        context = {
            'car_form': car_form,
        }
        return render(request, 'car_module/filtered_cars.html', context)

    def post(self, request):
        car_form = CarsFilterForm(request.POST)
        if car_form.is_valid():
            car_name = car_form.cleaned_data.get('car_name')
            VIN_number_from = car_form.cleaned_data.get('VIN_number_from')
            VIN_number_to = car_form.cleaned_data.get('VIN_number_to')
            cars = CarModel.objects.all()

            if car_name:
                cars = cars.filter(car_name__iexact=car_name)
            if VIN_number_from is not None:
                if VIN_number_to is not None:
                    cars = cars.filter(VIN_number__range=(VIN_number_from, VIN_number_to))
                else:
                    cars = cars.filter(VIN_number__gte=VIN_number_from)

            context = {
                'car_form': car_form,
                'filtered_car': cars,
            }
            return render(request, 'car_module/filtered_cars.html', context)

        context = {
            'car_form': car_form,
        }
        return render(request, 'car_module/filtered_cars.html', context)
