import random
import string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

from aplicatie2.models import Resorts  # , UserExtend  Pontaj,
from aplicatie2.forms import ResortsForm, ProfileForm  # , ProfileForm  # , NewAccountForm
import datetime


class ListResortView(LoginRequiredMixin, ListView):
    model = Resorts
    template_name = 'aplicatie2/resort_index.html'

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return self.model.objects.all()

        return self.model


class CreateResortView(LoginRequiredMixin, CreateView):
    model = Resorts

    form_class = ResortsForm
    template_name = 'aplicatie2/resorts_form.html'

    def get_form_kwargs(self):
        variable_to_send = super(CreateResortView, self).get_form_kwargs()
        variable_to_send.update({'pk': None})
        return variable_to_send

    def get_success_url(self):
        return reverse('aplicatie2:lista')


class UpdateResortView(LoginRequiredMixin, UpdateView):
    model = Resorts
    form_class = ResortsForm

    template_name = 'aplicatie2/resorts_form.html'

    def get_form_kwargs(self):
        variable_to_send = super(UpdateResortView, self).get_form_kwargs()
        variable_to_send.update({'pk': self.kwargs['pk']})
        return variable_to_send

    def get_success_url(self):
        return reverse('aplicatie2:lista')


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    profile_form = ProfileForm
    template_name = 'aplicatie2/profile.html'

    def post(self, request, *args, **kwargs):
        post_data = request.POST or None

        profile_form = ProfileForm(post_data, instance = request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse_lazy('aplicatie2:lista'))
        context = self.get_context_data(profile_form = profile_form)

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)











# class UpdateProfile(LoginRequiredMixin, UpdateView):
#     model = UserExtend
#     form_class = NewAccountForm
#     template_name = 'aplicatie2/resorts_form.html'
#
#     def get_queryset(self):
#         return self.model.objects.all()
#
#     def get_success_url(self):
#         return reverse('aplicatie2:lista')
#
#     def get_form_kwargs(self):
#         kwargs = super(UpdateProfile, self).get_form_kwargs()
#         kwargs.update({'current_user': self.request.user.id, 'action': 'update', 'pk': self.kwargs['pk']})
#         return kwargs
#
#
# punctuation = '!@#$%&*'


# class NewAccountView(LoginRequiredMixin, CreateView):
#     model = UserExtend
#     template_name = 'aplicatie1/location_form.html'
#     form_class = NewAccountForm
#
#     def get_form_kwargs(self):
#         kwargs = super(NewAccountView, self).get_form_kwargs()
#         kwargs.update({'current_user': self.request.user.id, 'action': 'create', 'pk': None})
#         return kwargs
#
#     def form_valid(self, form):
#         if form.is_valid():
#             form.save(commit = False)
#         return super(NewAccountView, self).form_valid(form)
#
#     def get_success_url(self):
#         psw = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
#                                                    string.ascii_lowercase +
#                                                    string.digits +
#                                                    punctuation) for _ in range(8))
#
#         if User.objects.filter(id = self.object.id).exists():
#             user_instance = User.objects.get(id = self.object.id)
#             user_instance.set_password(psw)
#             user_instance.username = f"{'.'.join(str(user_instance.first_name).split(' '))}.{'.'.join(user_instance.last_name.split(' '))}"
#             user_instance.save()
#             content_email = f"Username si parola : {user_instance.username} {psw}"
#             msg_html = render_to_string('emails/invite_user.html', {'content_email': content_email})
#             msg = EmailMultiAlternatives(subject = 'New account', body = content_email, from_email = 'contact@test.ro', to = [user_instance.email])
#             msg.attach_alternative(msg_html, 'text/html')
#             msg.send()
#         return reverse('aplicatie2:lista')
#
