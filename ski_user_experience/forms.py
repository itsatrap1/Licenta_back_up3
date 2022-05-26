from django import forms
from ski_user_experience.models import AdditionalInformationModel
from django.contrib.auth.models import User
from webscrapping.models import Resorts
from django_select2 import forms as select2_form


class ResortSelectWidget(select2_form.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains"
    ]


class AdditionallnfoModelForm(forms.ModelForm):

    class Meta:
        model = AdditionalInformationModel
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'resort_choice': ResortSelectWidget,
        }

    def __init__(self, pk, *args, **kwargs):

        pk_user = kwargs.pop('pk_user', None)
        super(AdditionallnfoModelForm, self).__init__(*args, **kwargs)
        self.pk = pk
        self.fields['user'].disabled = True
        self.fields['user'].initial = User.objects.last()

        for el in self.fields:
            self.fields[el].label = False

    def clean(self):
        return self.cleaned_data


