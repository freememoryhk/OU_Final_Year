from django import forms
from django.contrib.auth.forms import *;
from ou_fyp.models import *;
from django.contrib.auth.models import User;
from itertools import chain;
class TagsCreateForm(forms.ModelForm):
    class Meta:
        model = Tags;
        fields = ["tag_name"];
class DynamicMultipleChoiceField(forms.MultipleChoiceField):
    def validate(self, value):
        if self.required and not value:    
            raise ValidationError(self.error_messages['required'])
class TagMultiChoice(forms.CheckboxSelectMultiple):
    def __init__(self,attrs=None,acceptNewTag=False,rowSize=2):
        self.acceptNewTag= acceptNewTag;
        self.rowSize =rowSize;
        super(TagMultiChoice,self).__init__(attrs=attrs);
    def render(self,name,value,attrs=None,choices=()):
        #orgInput = super(TagMultiChoice,self).render(name,value,attrs,choices);
        contentInput = [];
        tagInput = "<input id='{0}'/><button id='{0}_btn'>Add Tag</button>".format("id_"+name+"_add");
        row=0;
        rowRemaining = self.rowSize;
        aviableToPut=[];
        if len(choices) == 0 and len(self.choices) == 0:
            contentInput.append("<ul id='row_{0}'><li>{1}</li></ul>".format(row,tagInput));
            rowRemaining-=1;
        else:
            if len(choices) == 0:
                choices = self.choices;
            else:
                self.choices = choices;
            for tag in TagsProxy().excludePopluarTagsList(self.choices):
                aviableToPut.append(tag.tag_name);
        jArrayForVal=[];
        for index,choice in enumerate(choices):
            choicesInput = "<li><input type=\"checkbox\" name=\"{0}\" id=\"id_{0}_{1}\" value=\"{2[1]}\"/><label for=\"id_{0}_{1}\">{2[1]}</label></li>".format(name,index,choice);
            jArrayForVal.append(choice[1]);
            if index % self.rowSize == 0:
                if index != 0:
                    contentInput.append("</ul>");
                contentInput.append("<ul id=\"row_{}\">".format(row));
                row+=1;
                rowRemaining = self.rowSize;
                if index == 0:
                    contentInput.append("<li>{0}</li>{1}".format(tagInput,choicesInput));
                else:
                    contentInput.append(choicesInput);
            else:
                if index < self.rowSize and index == self.rowSize -1 :
                    contentInput.append("{}<li>{}</li>".format(choicesInput,tagInput));
                else:
                    contentInput.append(choicesInput);
            rowRemaining-=1;
            if index + 1 == len(choices):
                row-=1;
                contentInput.append("</ul>");
        jsForInput = [];
        jsForInput.append("<script>");
        jsForInput.append("maxRow={};".format(row));
        jsForInput.append("perRowSize={};".format(self.rowSize));
        jsForInput.append("maxRowRemaining={};".format(rowRemaining));
        import json;
        jsForInput.append("existingTags={};".format(json.dumps(jArrayForVal)));
        jsForInput.append("avaiTags={};".format(json.dumps(aviableToPut)));
        jsForInput.append("$(document).ready");
        jsForInput.append("(");
        jsForInput.append("function()");
        jsForInput.append("{");
        #jsForInput += "$(\"#id_{}_checkbox_list\").buttonset();".format(name);
        #jsForInput.append("console.log(\"Auto Complete List:\"+avaiTags);");
        jsForInput.append("$(\"#id_{}_add\").autocomplete".format(name));
        jsForInput.append("(");
        jsForInput.append("{");
        jsForInput.append("source:avaiTags");
        if self.acceptNewTag == False:
            jsForInput.append(",change: function(event,ui)");
            jsForInput.append("{");
            #jsForInput.append("console.log(\"New Value\"+$(this).val())");
            jsForInput.append("if (avaiTags.indexOf($(this).val()) == -1)");
            jsForInput.append("{");
            jsForInput.append("$(this).trigger('keydown.autocomplete');");
            jsForInput.append("$(this).val(\"\")");
            jsForInput.append("}");
            jsForInput.append("}");
        jsForInput.append("}");
        jsForInput.append(");");
        jsForInput.append("$(\"#id_{}_add_btn\").click".format(name));
        jsForInput.append("(");
        jsForInput.append("function(event)");
        jsForInput.append("{");
        jsForInput.append("event.preventDefault();");
        #jsForInput.append("console.log($(\"#id_{}_checkbox_list\").html());".format(name));
        jsForInput.append("var tagField = $(\"#id_{}_add\")".format(name));
        jsForInput.append("var rowValue = tagField.val()");
        jsForInput.append("if (existingTags.indexOf(rowValue) != -1  || rowValue == \"\")");
        jsForInput.append("{");
        jsForInput.append("return;");
        jsForInput.append("}");
        jsForInput.append("var beforeNewRow = \"\";");
        jsForInput.append("var afterNewRow = \"\";");
        jsForInput.append("var attackDOM;");
        jsForInput.append("if (maxRowRemaining === 0 )");
        jsForInput.append("{");
        jsForInput.append("maxRow+=1;");
        jsForInput.append("maxRowRemaining=perRowSize;");
        jsForInput.append("beforeNewRow=\"<ul id='row_\"+maxRow+\"'>\";");
        jsForInput.append("afterNewRow=\"</ul>\";");
        jsForInput.append("attackDOM = $(\"#id_{}_checkbox_list\");".format(name));
        jsForInput.append("}");
        jsForInput.append("else");
        jsForInput.append("{");
        jsForInput.append("attackDOM = $(\"#row_\"+maxRow);");
        jsForInput.append("}");
        jsForInput.append("var rowIndex = (maxRow * perRowSize) +(perRowSize - maxRowRemaining)");
        jsForInput.append("var newRow =\"<li><input type='checkbox' checked='checked' name='{0}' id='id_{0}_\"+rowIndex+\"' value='\"+rowValue+\"'/><label for='id_{0}_\"+rowIndex+\"'>\"+rowValue+\"</label></li>\"".format(name));
        jsForInput.append("attackDOM.append(beforeNewRow+newRow+afterNewRow)");
        jsForInput.append("maxRowRemaining -= 1");
        jsForInput.append("existingTags.push(rowValue)");
        jsForInput.append("if (avaiTags.indexOf(rowValue) != -1 )");
        jsForInput.append("{");
        jsForInput.append("avaiTags.splice(avaiTags.indexOf(rowValue),1)");
        jsForInput.append("}");
        jsForInput.append("tagField.val(\"\")");
        #jsForInput.append("console.log(\"New Max Row Index\"+maxRow);");
        #jsForInput.append("console.log(\"New Row Size\"+perRowSize);");
        #jsForInput.append("console.log(\"New Max Row Remaining\"+maxRowRemaining);");
        jsForInput.append("}");
        jsForInput.append(")");
        jsForInput.append("}");
        jsForInput.append(");");
        jsForInput.append("</script>");
        from django.utils.safestring import mark_safe
        finalOutPut = [];
        #finalOutPut.append(cssForInput);
        finalOutPut.append("<div id=\"id_{}_checkbox_list\" class=\"litable\">".format(name));
        finalOutPut.append(mark_safe("\n".join(contentInput)));
        #finalOutPut.append(tagInput);
        finalOutPut.append("</div>");
        finalOutPut.append(mark_safe("\n".join(jsForInput)));
        return str(mark_safe("\n".join(finalOutPut)));
class CreateProjectForm(forms.ModelForm):
    #project_tags = forms.MultipleChoiceField(label="Project Tags");
    #project_contents = forms.FileField(label="STL content");
    def __init__(self,*args,**kwargs):
        super(CreateProjectForm,self).__init__(*args,**kwargs);
        tags = TagsProxy();
        popList = tags.popluarTagsList();
        #self.project_tags = forms.MultipleChoiceField(label="Project Tags",choices=popList);
        #self.project_contents = forms.FileField(label="STL content");
        self.fields["project_tags"] = DynamicMultipleChoiceField(widget=TagMultiChoice,label="Project Tags",choices=popList,required=False);
        self.fields["project_tags"].widget.acceptNewTag = True;
        self.fields["project_tags"].widget.rowSize = 5;
        self.fields["project_contents"] = forms.FileField(label="STL content",required=False);
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
