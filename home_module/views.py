from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class IndexView(View):
    def get(self, request):
        return render(request, 'home_module/home.html')
