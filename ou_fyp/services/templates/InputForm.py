from django import forms
from django.contrib.auth.forms import *;
from ou_fyp.models import *;
from django.contrib.auth.models import User;
class TagsCreateForm(forms.ModelForm):
    class Meta:
        model = Tags;
        fields = ["tag_name"];
class CreateProjectForm(forms.ModelForm):
    #project_tags = forms.MultipleChoiceField(label="Project Tags");
    #project_contents = forms.FileField(label="STL content");
    def __init__(self,*args,**kwargs):
        super(CreateProjectForm,self).__init__(*args,**kwargs);
        tags = TagsProxy();
        popList = tags.popluarTagsList();
        #self.project_tags = forms.MultipleChoiceField(label="Project Tags",choices=popList);
        #self.project_contents = forms.FileField(label="STL content");
        self.fields["project_tags"] = forms.MultipleChoiceField(label="Project Tags",choices=popList);
        self.fields["project_contents"] = forms.FileField(label="STL content");
        self.project_tags_autocomplete = tags.excludePopluarTagsList(popluarTagsTuple=popList);
    class Meta:
        model = ThreeDimensionsProjects;
        fields = ['project_description','price'];
        widgets = {"price":forms.TextInput(attrs={"type":"number","max":"99999.99","min":"0.00","step":"0.01","value":"0.00"})};
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
