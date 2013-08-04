# Create your views here.
from django.http import HttpResponse
from django.template import Context,Template,loader
from ou_fyp.services.AbstractView import *;
from ou_fyp.services.templates.InputForm import RegisterForm;
from django.contrib.auth.models import User,Group;
from django.core.context_processors import csrf;
class UserParameterReader(AbstractParameterReader):
    def __init__(self,request):
        super().__init__(request);
        self.projectId = self.request.getParameter("id",acceptNone=True);
class UserViews(AbstractView):
    def __init__(self,request):
        super().__init__(request);
        self.setReaderStratedy(UserParameterReader);
    def register(self):
        uf = RegisterForm();
        templateObj = loader.get_template("register.html");
        fill = dict(list(csrf(self.request.request).items())+list({"form":uf,"title":"Register to system","submitLink":self.submitLink}.items()))
        context= Context(fill);
        return templateObj.render(context);    
