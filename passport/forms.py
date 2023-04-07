from django import forms


class UpdatePersonalInfoForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(widget=forms.EmailInput(), required=False)
    number_of_phone = forms.IntegerField(max_value=99999999999)
    date_of_birthday = forms.DateField(widget=forms.DateInput())
    city = forms.CharField()
    address = forms.CharField()


class GetBiometriaForm(forms.Form):
    ...
