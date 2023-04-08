from django import forms


class UpdatePersonalInfoForm(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': "Имя"}), label='Имя')
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': "Фамилия"}),
                                label="Фамилия")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Придумайте пароль"}), label='Пароль')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': "Email"}), required=False, label='Email')
    number_of_phone = forms.IntegerField(max_value=99999999999,
                                         widget=forms.NumberInput(attrs={'placeholder': "Ваш номер телефона"}),
                                         label='Номер телефона')
    date_of_birthday = forms.CharField(widget=forms.DateInput(attrs={'placeholder': "Дата рождения"}),
                                       label='Дата рождения')
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Город проживания"}), label='Город проживания')
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Адрес проживания"}),
                              label='Адрес проживания')


class CreateUserForm(UpdatePersonalInfoForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Логин"}), label='Логин')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "Подтвердите пароль"}),
                                       label='Подтвердите пароль')


class GetBiometriaForm(forms.Form):
    ...
