from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView

from ski_user_experience.forms import AdditionallnfoModelForm
from ski_user_experience.models import AdditionalInformationModel
from webscrapping.models import Resorts


class CreateInfoView(CreateView):
    model = AdditionalInformationModel

    form_class = AdditionallnfoModelForm
    template_name = "ski_user_experience/additional_info.html"

    def get_form_kwargs(self):
        variable_to_send = super(CreateInfoView, self).get_form_kwargs()
        variable_to_send.update({'pk': None})
        variable_to_send.update({'pk_user': self.request.user.id})
        return variable_to_send

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['resort_list'] = Resorts.objects.filter(name)
    #     return context

    def get_success_url(self):
        return reverse('login')


