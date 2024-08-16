from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('all_reports/<str:car_name>/<str:VIN_number>/', views.ReportListView.as_view(), name='reports'),
    path('add_report/<str:car_name>/<str:car_VIN>/', views.AddReportsView.as_view(), name='add-report'),
    path('<str:car_name>/<int:car_VIN>/<int:pk>/', views.ReportsUpdateView.as_view(), name='report-detail'),
    path('delete/<str:car_name>/<int:car_VIN>/<int:pk>/', views.ReportDeleteView.as_view(), name='report-delete'),
    path('autocomplete-defect-code-appearance/', views.autocomplete_defect_code_appearance,
         name='autocomplete-defect-code-appearance'),
    path('autocomplete-defect-code-functionality/', views.autocomplete_defect_code_functionality,
         name='autocomplete-defect-code-functionality'),
    path('autocomplete-defect-part/', views.autocomplete_defect_part, name='autocomplete-defect-part'),
]
