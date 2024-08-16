from django.shortcuts import render, redirect, get_object_or_404
from car_module.models import CarModel
from django.views import View
from .forms import ReportsModelForm, NumReportsForm, ReportsFilterForm, CAR_PARTS, defect_code_functionality
from .forms import defect_code_appearance
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpRequest, HttpResponse
from .models import ReportsModel
import pandas as pd
from jalali_date import date2jalali
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def autocomplete_defect_code_appearance(request):
    term = request.GET.get('term')
    queryset = ReportsModel.objects.filter(defect_code_appearance__icontains=term)
    data = list(queryset.values('id', 'defect_code_appearance'))
    return JsonResponse(data, safe=False)


def autocomplete_defect_code_functionality(request):
    term = request.GET.get('term')
    queryset = ReportsModel.objects.filter(defect_code_functionality__icontains=term)
    data = list(queryset.values('id', 'defect_code_functionality'))
    return JsonResponse(data, safe=False)


def autocomplete_defect_part(request):
    print('hello')
    term = request.GET.get('term')
    queryset = ReportsModel.objects.filter(defect_part__icontains=term)
    data = list(queryset.values('id', 'defect_part'))
    return JsonResponse(data, safe=False)


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    def get(self, request):
        return render(request, 'rework_module/index.html')


@method_decorator(login_required, name='dispatch')
class ReportListView(View):
    def get(self, request, car_name, VIN_number):
        car: CarModel = CarModel.objects.filter(car_name__iexact=car_name, VIN_number__exact=VIN_number).first()
        if not car:
            # Handle the case where the car is not found
            return render(request, 'rework_module/All_Reports.html', {
                'error': 'Car not found',
                'car_name': car_name,
                'car_VIN': VIN_number,
            })

        reports = ReportsModel.objects.filter(car_name__iexact=car_name, car_IN=car)
        context = {
            'reports': reports,
            'car_name': car.car_name,
            'car_VIN': car.VIN_number
        }
        return render(request, 'rework_module/All_Reports.html', context)


@method_decorator(login_required, name='dispatch')
class AddReportsView(View):
    def get(self, request, car_name, car_VIN):
        num_reports_form = NumReportsForm()
        num_reports = request.GET.get('num_reports', 1)
        ReportsFormSet = modelformset_factory(ReportsModel, form=ReportsModelForm, extra=int(num_reports))
        formset = ReportsFormSet(queryset=ReportsModel.objects.none())

        # Pass car_name to each form in the formset
        for form in formset:
            form.fields['defect_part'].choices = [(part, part) for part in CAR_PARTS.get(car_name, [])]

        context = {
            'num_reports_form': num_reports_form,
            'formset': formset,
            'car_name': car_name,
            'car_VIN': car_VIN
        }
        return render(request, 'rework_module/Reports.html', context)

    def post(self, request: HttpRequest, car_name, car_VIN):
        if 'num_reports' in request.POST:
            num_reports_form = NumReportsForm(request.POST)
            if num_reports_form.is_valid():
                num_reports = num_reports_form.cleaned_data['num_reports']
                return redirect(f'{request.path}?num_reports={num_reports}')
        else:
            ReportsFormSet = modelformset_factory(ReportsModel, form=ReportsModelForm)
            formset = ReportsFormSet(request.POST)

            # Pass car_name to each form in the formset
            for form in formset:
                form.fields['defect_part'].choices = [(part, part) for part in CAR_PARTS.get(car_name, [])]
                form.fields['defect_code_appearance'].choices = [(code, code) for code in defect_code_appearance]
                form.fields['defect_code_fuctionality'].choices = [(code, code) for code in defect_code_functionality]

            if formset.is_valid():
                instances = formset.save(commit=False)
                car = get_object_or_404(CarModel, car_name=car_name, VIN_number=car_VIN)
                for instance in instances:
                    instance.person = request.user
                    instance.car_name = car.car_name
                    instance.car_IN = car
                    instance.save()
                return redirect('reports', car_name=car_name, VIN_number=car_VIN)
        context = {
            'formset': formset,
        }
        return render(request, 'rework_module/Reports.html', context)


@method_decorator(login_required, name='dispatch')
class ReportsUpdateView(View):
    def get(self, request, car_name, car_VIN, pk):
        car = get_object_or_404(CarModel, car_name=car_name, VIN_number=car_VIN)
        report = get_object_or_404(ReportsModel, car_name=car_name, car_IN=car, pk=pk)
        report_form = ReportsModelForm(instance=report)
        context = {
            'report': report_form,
            'car_name': car.car_name,
            'car_IN': car.VIN_number,
            'person': report.person,
            'date': date2jalali(report.error_date)
        }
        return render(request, 'rework_module/report_detail.html', context)

    def post(self, request: HttpRequest, car_name, car_VIN, pk):
        car = get_object_or_404(CarModel, car_name=car_name, VIN_number=car_VIN)
        report = get_object_or_404(ReportsModel, car_name=car_name, car_IN=car, pk=pk)
        report_form = ReportsModelForm(request.POST, instance=report)
        if report_form.is_valid():
            report_form.save()
            return redirect('reports', car_name=car.car_name, VIN_number=car.VIN_number)
        else:
            context = {
                'car_form': report_form,
                'form_errors': report_form.errors,
            }
            return render(request, 'rework_module/report_detail.html', context)


@method_decorator(login_required, name='dispatch')
class ReportDeleteView(View):
    def get(self, request, car_name, car_VIN, pk):
        car = get_object_or_404(CarModel, car_name=car_name, VIN_number=car_VIN)
        report = get_object_or_404(ReportsModel, car_name=car_name, car_IN=car, pk=pk)
        if report:
            report.delete()
            return redirect('reports', car_name=car.car_name, VIN_number=car.VIN_number)
        else:
            return redirect('reports', car_name=car.car_name, VIN_number=car.VIN_number)


@method_decorator(login_required, name='dispatch')
class FilterReportsView(View):
    def get(self, request):
        report_form = ReportsFilterForm()
        context = {
            'report_form': report_form,
        }
        return render(request, 'rework_module/filtered_reports.html', context)

    def post(self, request):
        report_form = ReportsFilterForm(request.POST)
        if report_form.is_valid():
            car_name = report_form.cleaned_data.get('car_name')
            VIN_number_from = report_form.cleaned_data.get('VIN_number_from')
            VIN_number_to = report_form.cleaned_data.get('VIN_number_to')
            start_date = report_form.cleaned_data.get('start_date')
            end_date = report_form.cleaned_data.get('end_date')
            grade = report_form.cleaned_data.get('grade')
            zone = report_form.cleaned_data.get('zone')
            defect_code_appearance = report_form.cleaned_data.get('defect_code_appearance')
            defect_code_functionality = report_form.cleaned_data.get('defect_code_functionality')
            defect_part = report_form.cleaned_data.get('defect_part')
            defect_origin = report_form.cleaned_data.get('defect_origin')
            defect_fix_time = report_form.cleaned_data.get('defect_fix_time')
            changed = report_form.cleaned_data.get('changed')

            reports = ReportsModel.objects.all()
            if car_name:
                reports = reports.filter(car_IN__car_name__iexact=car_name)
            if VIN_number_from and VIN_number_to:
                reports = reports.filter(car_IN__VIN_number__range=(VIN_number_from, VIN_number_to))
            if start_date:
                reports = reports.filter(error_date__date__gte=start_date)
            if end_date:
                reports = reports.filter(error_date__date__lte=end_date)
            if grade:
                reports = reports.filter(grade__iexact=grade)
            if zone:
                reports = reports.filter(zone__iexact=zone)
            if defect_code_appearance:
                reports = reports.filter(defect_code_appearance__iexact=defect_code_appearance)
            if defect_code_functionality:
                reports = reports.filter(defect_code_fuctionality__iexact=defect_code_functionality)
            if defect_part:
                reports = reports.filter(defect_part__iexact=defect_part)
            if defect_origin:
                reports = reports.filter(defect_origin__iexact=defect_origin)
            if defect_fix_time:
                reports = reports.filter(defect_fix_time__exact=defect_fix_time)
            if changed is not None:
                reports = reports.filter(changed=changed)
            if changed is None:
                reports = reports.all()

            if 'export_to_excel' in request.POST:
                return self.export_to_excel(reports, start_date, end_date)

            context = {
                'report_form': report_form,
                'filtered_reports': reports,
            }
            return render(request, 'rework_module/filtered_reports.html', context)

        context = {
            'report_form': report_form,
        }
        return render(request, 'rework_module/filtered_reports.html', context)

    def export_to_excel(self, queryset, start_date, end_date):
        data = []
        for report in queryset:
            # Convert timezone-aware datetime to timezone-unaware datetime
            error_date_naive = report.error_date.replace(tzinfo=None)
            if report.changed is True:
                report.changed = 'بله'
            if report.changed is False:
                report.changed = 'خیر'
            data.append([
                report.car_IN.car_name,
                report.car_IN.VIN_number,
                report.person,
                date2jalali(error_date_naive),
                report.grade,
                report.zone,
                report.defect_code_appearance,
                report.defect_code_fuctionality,
                report.defect_part,
                report.defect_origin,
                report.defect_fix_time,
                report.reworker_action,
                report.changed
            ])

        df = pd.DataFrame(data, columns=[
            'نام ماشین', 'VIN شماره', 'پرسنل ثبت کننده', 'تاریخ ثبت', 'گرید', 'منطقه محل وقوع',
            'نوع ایراد ظاهری', 'نوع ایراد عملکردی',
            'شرح قطعه', 'منشا خطا', 'زمان رفع ایراد(دقیقه)', 'عملکرد ریورکر',
            'قطعه تعویض شده'
        ])
        # Format the filename with date range
        if start_date and end_date:
            start_date_str = date2jalali(start_date).strftime('%y/%m/%d') if start_date else f'start:{date2jalali(data[4])}'
            end_date_str = date2jalali(end_date).strftime('%y/%m/%d') if end_date else f'end:{date2jalali(data[4])}'
            filename = f'reports_{start_date_str}_to_{end_date_str}.xlsx'
        else:
            filename = 'reports.xlsx'

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        df.to_excel(response, index=False, engine='openpyxl')

        return response
