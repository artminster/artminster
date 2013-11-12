from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from allauth.account.forms import LoginForm

from utils import get_auth_profile_class

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    
    class Meta:
        model = get_auth_profile_class()
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['email'].initial = self.instance.user.email
        
    def save(self, *args, **kwargs):
        profile = super(UserProfileForm, self).save(*args, **kwargs)
        profile.user.first_name = self.cleaned_data.get('first_name')
        profile.user.last_name = self.cleaned_data.get('last_name')
        profile.user.email = self.cleaned_data.get('email')
        profile.user.save()
        return profile
        

"""class ProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = UserProfile
        fields = ()

        widgets = {
            'photo': forms.FileInput(),
        }
        

    helper = FormHelper()
        
    helper.form_tag = False
    layout = Layout(
        Fieldset('',
            'first_name',
            'last_name',
        ),
    )

    helper.add_layout(layout)

class SignupForm(forms.ModelForm):
    first_name = forms.CharField( max_length = 25)
    last_name = forms.CharField( max_length = 25)
    email = forms.EmailField( max_length = 255)
    preferred_username = forms.RegexField( min_length = 5, max_length = 30, required = False, regex=r'^\w+$', label="Username")
    password1 = forms.CharField(label="Password", min_length = 5, max_length = 30, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat password", min_length = 5, max_length = 30, widget=forms.PasswordInput)

    helper = FormHelper()
    helper.form_tag = False

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(_(u"This email already registered."))

        return email

    def clean_password2(self):
        passwd1 = self.cleaned_data['password1']
        passwd2 = self.cleaned_data['password2']
        if passwd1 != passwd2:
            raise forms.ValidationError(_(u'Passwords should match'))

        return passwd1

    def clean_preferred_username(self):
        username = self.cleaned_data['preferred_username']
        if username and User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError(_(u"User with username %(username)s "\
                u"already exist. Please, choose another username.") % {
            'username': username,
            })

        return username

    def save(self, commit=True, request=None):
        user = super(SignupForm, self).save(commit=False)
        username = self.cleaned_data['preferred_username']
        user.username = username
        if not username or \
                User.objects.filter(username=username).count() > 0:
            username = user.email.split('@')[0]
            username_cnt = 1
            username_cur = "%s-%d" % (username, username_cnt)
            while User.objects.filter(username=username_cur).count() > 0:
                username_cur = "%s-%d" % (username, username_cnt)
                username_cnt += 1
                if username_cnt > 10:
                    raise forms.ValidationError("Can't generate username")

            user.username = username_cur
        
        new_pass =  self.cleaned_data['password1']
        if new_pass:
            user.set_password(new_pass)
        user.save()
        
        profile = user.profile
        profile.save()
        
        return user

    layout = Layout(
        # second fieldset shows the contact info
        Fieldset('',
            Row('first_name', 'last_name'),
            Row('email', 'preferred_username'),
            Row('password1', 'password2'),
        ),
    )

    helper.add_layout(layout)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'preferred_username', 'password1', 'password2',)"""