from django import forms


class UpdatePersonalInfoForm(forms.Form):
    first_name = forms.CharField(required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), label='Имя')
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
                                label="Фамилия")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
                               label='Пароль')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'}), required=False,
                             label='Email')
    number_of_phone = forms.IntegerField(max_value=99999999999,
                                         widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'}),
                                         label='Номер телефона')

    date_of_birthday = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
                                       label='Дата рождения')
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
                           label='Город проживания')
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
                              label='Адрес проживания')


class CreateUserForm(UpdatePersonalInfoForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), label='Логин')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
                                       label='Подтвердите пароль')


class GetBiometriaForm(forms.Form):
    ...
