from django.urls import path
from . import views
from rework_module.views import FilterReportsView

urlpatterns = [
    path('', views.CarListView.as_view(), name='car-list'),
    path('cars_list/', views.CarListView.as_view(), name='car-list'),
    path('add_car/', views.CarAddView.as_view(), name='add-car'),
    path('<str:car_name>/<int:VIN_number>/', views.CarDetailView.as_view(), name='car-detail'),
    path('edit/<str:car_name>/<int:VIN_number>/', views.CarUpdateView.as_view(), name='car-update'),
    path('delete/<str:car_name>/<int:VIN_number>/', views.CarDeleteView.as_view(), name='car-delete'),
    path('filter/', views.FilterCarView.as_view(), name='filter_cars'),
    path('filter_reports/', FilterReportsView.as_view(), name='filter_reports'),

]
