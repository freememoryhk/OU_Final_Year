# Create your views here.
from django.http import HttpResponse
<<<<<<< HEAD
from django.template import Template,loader
from django.template import RequestContext as Context
from ou_fyp.services.AbstractView import *;
from ou_fyp.services.templates.InputForm import *;
from django.contrib.auth.models import User,Group;
#from django.core.context_processors import csrf;
=======
from django.template import Context,Template,loader
from ou_fyp.services.AbstractView import *;
from ou_fyp.services.templates.InputForm import RegisterForm;
from django.contrib.auth.models import User,Group;
from django.core.context_processors import csrf;
>>>>>>> 495fa86ea5d97b89dda4e984fe58b68040564eed
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
<<<<<<< HEAD
        #fill = dict(list(csrf(self.request.request).items())+list({"form":uf,"title":"Register to system","submitLink":self.submitLink}.items()))
        fill = {"form":uf,"noajax":True,"title":"Register to system","submitLink":self.submitLink};
        context= Context(self.request.request,fill);
        return templateObj.render(context);    
    def login(self):
        ul = LoginForm();
        context= Context(self.request.request,fill);
        return templateObj.render(context);
=======
        fill = dict(list(csrf(self.request.request).items())+list({"form":uf,"title":"Register to system","submitLink":self.submitLink}.items()))
        context= Context(fill);
        return templateObj.render(context);    
>>>>>>> 495fa86ea5d97b89dda4e984fe58b68040564eed
