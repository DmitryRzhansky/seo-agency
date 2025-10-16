from django import forms
from .models import ContactRequest

class ContactForm(forms.ModelForm):
    """Форма обратной связи для главной страницы."""
    
    # Мы переопределяем поля, чтобы добавить Bootstrap классы
    name = forms.CharField(
        label='Ваше имя', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )
    phone = forms.CharField(
        label='Телефон', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (XXX) XXX-XX-XX'})
    )
    email = forms.EmailField(
        label='Email (Необязательно)', 
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'})
    )
    message = forms.CharField(
        label='Сообщение / Подробности проекта', 
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишите ваш проект или вопрос'})
    )

    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'message']
