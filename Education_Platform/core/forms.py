from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Profile

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="اسم المستخدم",
        help_text="مطلوب. 150 حرفًا أو أقل. يمكن استخدام الأحرف والأرقام و@/./+/-/_ فقط."
    )
    password1 = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput,
        help_text="• يجب أن تحتوي على 8 أحرف على الأقل.<br>"
                  "• لا يمكن أن تكون شائعة الاستخدام.<br>"
                  "• لا يمكن أن تكون مكونة من أرقام فقط."
    )
    password2 = forms.CharField(
        label="تأكيد كلمة المرور",
        widget=forms.PasswordInput,
        help_text="أدخل كلمة المرور نفسها مرة أخرى للتحقق."
    )
    email = forms.EmailField(
        label="البريد الإلكتروني",
        required=True
    )
    first_name = forms.CharField(
        label="الاسم الأول",
        required=True
    )
    last_name = forms.CharField(
        label="اسم العائلة",
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="اسم المستخدم",
    )
    password = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput
    )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'profile_picture']
        labels = {
            'full_name': 'الاسم الكامل',
            'bio': 'نبذة شخصية',
            'profile_picture': 'الصورة الشخصية',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
