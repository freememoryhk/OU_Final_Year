# Create your views here.
from django.http import HttpResponse
from django.template import Template,loader
from django.template import RequestContext as Context
from ou_fyp.services.AbstractView import *;
from ou_fyp.services.templates.InputForm import *;
from django.contrib.auth.models import User,Group;
#from django.core.context_processors import csrf;
class UserParameterReader(AbstractParameterReader):
    def __init__(self,request):
        super().__init__(request);
        self.projectId = self.request.getParameter("id",acceptNone=True);
        self.next = self.request.getParameter("next",acceptNone=True);
class UserViews(AbstractView):
    def __init__(self,request):
        super().__init__(request);
        self.setReaderStratedy(UserParameterReader);
    def register(self):
        uf = RegisterForm();
        templateObj = loader.get_template("register.html");
        #fill = dict(list(csrf(self.request.request).items())+list({"form":uf,"title":"Register to system","submitLink":self.submitLink}.items()))
        fill = {"form":uf,"noajax":True,"title":"Register to system","submitLink":self.submitLink};
        context= Context(self.request.request,fill);
        return templateObj.render(context);    
    def login(self):
        from django.contrib.auth.forms import AuthenticationForm
        ul = AuthenticationForm();
        templateObj = loader.get_template("login.html");
        fill = {"form":ul,"noajax":True,"title":"Login to system","submitLink":self.submitLink};
        fill["next"] = self.parsReader.next;
        context= Context(self.request.request,fill);
        return templateObj.render(context);    
