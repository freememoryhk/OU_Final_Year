# Create your views here.
#from django.http import HttpResponse
#from django.template import Context,Template,loader
from django.http import HttpResponse
#from django.template import Context,Template,loader
from ou_fyp.services.AbstractView import *;
from django.contrib.auth.models import User,Group;
from django.contrib.auth import login;
from django.http import HttpResponseRedirect;
class UserParameterReader(AbstractParameterReader):
    def __init__(self,request):
        super().__init__(request);
        self.projectId = self.request.getParameter("id",acceptNone=True);
        self.next = self.request.getParameter("next",default="/tag/create");
class UserViews(AbstractView):
    def __init__(self,request):
        super().__init__(request);
        self.setReaderStratedy(UserParameterReader);
    def register(self):
        from ou_fyp.services.templates.InputForm import RegisterForm;
        uf = RegisterForm(self.request.request.POST);
        if uf.is_valid():
            u = uf.save(commit=False);
            u.set_password(u.password);
            u.save();
            g = Group();
            g.name = u.username;
            g.save();
            u.groups.add(g);
            u.save();
            if not self.request.request.is_ajax():
                return HttpResponseRedirect("/user/login");
    def login(self):
        from django.contrib.auth.forms import AuthenticationForm;
        ul = AuthenticationForm(data=self.request.request.POST);
        if ul.is_valid():
            login(self.request.request,ul.get_user());
            if not self.request.request.is_ajax():
                return HttpResponseRedirect(self.parsReader.next);
        else:
            if not self.request.request.is_ajax():
                return HttpResponseRedirect(self.viewLink);