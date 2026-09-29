from django.contrib.auth import login, logout
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import AgentPhoneNumbers


class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, required=True,
        label="Telefon",
        help_text="Masalan +998901234567"
    )
    email = forms.EmailField(required=False, label="Email (ixtiyoriy)")
    first_name = forms.CharField(max_length=150, label="Ism")
    last_name = forms.CharField(max_length=150, label="Familiya")
    is_staff = forms.BooleanField(required=False, label="Men agentman")

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'phone_number',
            'email', 'password1', 'password2', 'is_staff',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'masalan: jahongir_88', 'autocomplete': 'username',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'jahongir@example.com', 'autocomplete': 'email',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Kamida 8 ta belgi', 'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Parolni takrorlang', 'autocomplete': 'new-password',
        })


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    form.fields['username'].widget.attrs.update({
        'placeholder': 'Username', 'autocomplete': 'username',
    })
    form.fields['password'].widget.attrs.update({
        'placeholder': 'Parol', 'autocomplete': 'current-password',
    })
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'login.html', {'form': form})


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.is_staff = bool(form.cleaned_data.get('is_staff'))
        user.first_name = form.cleaned_data.get('first_name', '')
        user.last_name = form.cleaned_data.get('last_name', '')
        user.email = form.cleaned_data.get('email', '')
        user.save()
        phone = form.cleaned_data.get('phone_number')
        if phone:
            AgentPhoneNumbers.objects.create(user=user, phone_number=phone)
        login(request, user)
        return redirect('home')
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
