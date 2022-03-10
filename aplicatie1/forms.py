from django import forms

from aplicatie1.models import Location


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['city', 'country']

    def __init__(self, pk, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.pk = pk

    def clean(self):
        cleaned_data = self.cleaned_data
        city_value = cleaned_data.get('city')
        country_value = cleaned_data.get('country')

        if self.pk:
            if Location.objects.filter(city__icontains = city_value, country__icontains = country_value).exclude(id = self.pk).exists():
                self._errors['city'] = self.error_class(['Orasul si tara deja exista!'])
        else:
            if Location.objects.filter(city__icontains = city_value, country__icontains = country_value, active = 1).exists():
                self._errors['city'] = self.error_class(['Orasul si tara deja exista!'])

        return cleaned_data