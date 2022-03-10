from django import forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField

from aplicatie2.models import Companies, UserExtend


class CompaniesForm(forms.ModelForm):

    class Meta:

        model = Companies
        fields = '__all__'

    def __init__(self, pk,  *args, **kwargs):
        super(CompaniesForm, self).__init__(*args, **kwargs)
        self.company_pk = pk

    def clean(self):
        cleaned_data = self.cleaned_data
        name_value = cleaned_data.get('name')
        if self.company_pk:
            if Companies.objects.filter(name = name_value).exclude(id = self.company_pk).exists():
                self._errors['name'] = self.error_class(['Numele deja exista'])
        else:
            if Companies.objects.filter(name=name_value).exists():
                self._errors['name'] = self.error_class(['Numele deja exista'])

        return cleaned_data


class NewAccountForm(forms.ModelForm):
    class Meta:
        model = UserExtend
        fields = ['first_name', 'last_name', 'email', 'customer']

    def __init__(self, current_user, action, pk, *args, **kwargs):
        super(NewAccountForm, self).__init__(*args, **kwargs)
        self.action = action
        self.pk = pk
        user_instance = User.objects.get(id=current_user)
        if user_instance.is_superuser is False and UserExtend.objects.filter(id=current_user).exists():
            user_extend_instance = UserExtend.objects.get(id=current_user)
            self.fields['customer'] = ModelChoiceField(queryset=Companies.objects
                                                       .filter(id=user_extend_instance.customer.id))

    def clean(self):
        cleaned_data = self.cleaned_data
        email_value = cleaned_data.get('email')
        if self.action == 'create':
            if UserExtend.objects.filter(email=email_value).exists():
                self._errors['email'] = self.error_class(["Emaiul deja exista, te rugam sa alegi altul"])
        elif self.action == 'update':
            if UserExtend.objects.filter(email=email_value).exclude(id=self.pk).exists():
                self._errors['email'] = self.error_class(["Emaiul deja exista, te rugam sa alegi altul"])
        return cleaned_data

