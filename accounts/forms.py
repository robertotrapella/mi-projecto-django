from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """Formulario para editar campos del modelo User."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }


class ProfileUpdateForm(forms.ModelForm):
    """Formulario para editar campos del modelo Profile."""

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'bio': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Cuéntanos sobre ti...'}
            ),
        }