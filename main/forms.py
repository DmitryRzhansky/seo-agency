from django import forms

class ContactForm(forms.Form):
    """
    Форма для сбора заявок на консультацию.
    """
    # CharField для имени
    name = forms.CharField(
        max_length=100,
        label='Ваше имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )
    
    # CharField для телефона, с требованием валидации (например, min/max length)
    phone = forms.CharField(
        max_length=20,
        label='Телефон',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'})
    )
    
    # EmailField для адреса почты
    email = forms.EmailField(
        label='Email',
        required=False, # Сделаем его необязательным, если пользователь не хочет его указывать
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (необязательно)'})
    )
    
    # CharField или TextField для сообщения
    message = forms.CharField(
        label='Краткое описание задачи',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишите вашу задачу'})
    )