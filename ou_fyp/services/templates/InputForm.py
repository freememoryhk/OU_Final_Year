from django import forms
from django.contrib.auth.forms import *;
from ou_fyp.models import *;
from django.contrib.auth.models import User;
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User;
        fields = ['username','first_name','last_name','email','password'];
        widgets = {"email":forms.TextInput(attrs={"type":"email"}),"password":forms.PasswordInput()};
"""
class HolderForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(HolderForm,self).__init__(*args,**kwargs)
        passwordChoices=();
        accountChoices=();
        siteChoices=();
        for p in Passwords.objects.all():
            from passwordholder.myClass.pw import RandomPW;
            pwGen = RandomPW();
            pwGen.getInfoFromDB(p);
            passwordChoices = passwordChoices +((p.password_id,pwGen.getPW()),);
        for a in Account.objects.all():
            accountChoices = accountChoices + ((a.account_id,a.account),);
        for s in Sites.objects.all():
            siteChoices = siteChoices + ((s.site_id,s.site),);
        self.fields["site"] = ChoiceField(choices=siteChoices);
        self.fields["account"] = ChoiceField(choices=accountChoices);
        self.fields["password"] = ChoiceField(choices=passwordChoices);
    class Meta:
        model = Holders;
        fields = ['site','account','password'];
"""
