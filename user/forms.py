from django import forms

class loginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı adı")
    password = forms.CharField(label="Parola",widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50,label="Kullanıcı adı")
    password = forms.CharField(max_length=25,label="Parola",widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=25,label="Parolayı doğrula",widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password != confirm:
            raise forms.ValidationError("Parola eşleşmiyor.")

        else:
            values = {
                "username":username,
                "password":password
            }
            return values
