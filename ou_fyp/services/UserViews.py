# Create your views here.
#from django.http import HttpResponse
#from django.template import Context,Template,loader
from django.http import HttpResponse
from django.template import Context,Template,loader
from ou_fyp.services.AbstractView import *;
from django.contrib.auth.models import User,Group;
from django.http import HttpResponseRedirect;
class UserParameterReader(AbstractParameterReader):
    def __init__(self,request):
        super().__init__(request);
        self.projectId = self.request.getParameter("id",acceptNone=True);
class UserViews(AbstractView):
    def __init__(self,request):
        super().__init__(request);
        self.setReaderStratedy(UserParameterReader);
    def register(self):
        from ou_fyp.services.templates.InputForm import RegisterForm;
        uf = RegisterForm(self.request.request.POST);
        if uf.is_valid():
            u = uf.save();
            g = Group();
            g.name = u.username;
            g.save();
            u.groups.add(g);
            u.save();
            if self.request.request.is_ajax():
                return self.simpleOutPut();
            else:
                return HttpResponseRedirect(self.viewLink);
    def login():
        from django.contrib.auth.forms import AuthenticationForm;
        ul = AuthenticationForm(self.request.request.POST);
        if ul.is_valid():
            if self.request.request.is_ajax():
                return self.simpleOutPut();

        """
        u = User().objects.create_user(self.parsReader.uname,self.parsReader.email,self.parsReader.pw);
        u.first_name = self.parsReader.fname;
        u.last_name = self.parsReader.lname;
        u.save();
        """
