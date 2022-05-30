from django import forms
from django.contrib.auth.models import User
from aplicatie2.models import ResortUserRating
from webscrapping.models import Resorts


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class AddRatingForm(forms.ModelForm):
    class Meta:

        model = ResortUserRating
        fields = '__all__'

        widgets = {
            'resort_rating': forms.RadioSelect()
        }

    def __init__(self, pk,  *args, **kwargs):
        super(AddRatingForm, self).__init__(*args, **kwargs)
        self.pk = pk
        self.fields['user'].initial = self.pk

    def clean(self):
        return self.cleaned_data

# class ResortsForm(forms.ModelForm):
#
#     class Meta:
#
#         model = Resorts
#         fields = '__all__'
#
#     def __init__(self, pk,  *args, **kwargs):
#         super(ResortsForm, self).__init__(*args, **kwargs)
#         self.resort_pk = pk
#
#     def clean(self):
#         cleaned_data = self.cleaned_data
#         name_value = cleaned_data.get('name')
#         if self.company_pk:
#             if Resorts.objects.filter(name = name_value).exclude(id = self.resort_pk).exists():
#                 self._errors['name'] = self.error_class(['Numele deja exista'])
#         else:
#             if Resorts.objects.filter(name = name_value).exists():
#                 self._errors['name'] = self.error_class(['Numele deja exista'])
#
#         return cleaned_data


# class NewAccountForm(forms.ModelForm):
#     class Meta:
#         model = UserExtend
#         fields = ['first_name', 'last_name', 'email', 'customer']
#
#     def __init__(self, current_user, action, pk, *args, **kwargs):
#         super(NewAccountForm, self).__init__(*args, **kwargs)
#         self.action = action
#         self.pk = pk
#         user_instance = User.objects.get(id=current_user)
#         if user_instance.is_superuser is False and UserExtend.objects.filter(id=current_user).exists():
#             user_extend_instance = UserExtend.objects.get(id=current_user)
#             self.fields['customer'] = ModelChoiceField(queryset=Resorts.objects
#                                                        .filter(id=user_extend_instance.customer.id))
#
#     def clean(self):
#         cleaned_data = self.cleaned_data
#         email_value = cleaned_data.get('email')
#         if self.action == 'create':
#             if UserExtend.objects.filter(email=email_value).exists():
#                 self._errors['email'] = self.error_class(["Emaiul deja exista, te rugam sa alegi altul"])
#         elif self.action == 'update':
#             if UserExtend.objects.filter(email=email_value).exclude(id=self.pk).exists():
#                 self._errors['email'] = self.error_class(["Emaiul deja exista, te rugam sa alegi altul"])
#         return cleaned_data
#
