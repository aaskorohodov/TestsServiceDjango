from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from TestsGUI.models import Test


@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'TestsGUI/main-page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # noinspection PyUnresolvedReferences
        tests = Test.objects.all()
        context['tests'] = tests

        return context


def logout_user(request):
    logout(request)

    return redirect('home')
