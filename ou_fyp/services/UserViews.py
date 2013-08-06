# Create your views here.
<<<<<<< HEAD
#from django.http import HttpResponse
#from django.template import Context,Template,loader
=======
from django.http import HttpResponse
from django.template import Context,Template,loader
>>>>>>> 495fa86ea5d97b89dda4e984fe58b68040564eed
from ou_fyp.services.AbstractView import *;
from django.contrib.auth.models import User,Group;
class UserParameterReader(AbstractParameterReader):
    def __init__(self,request):
        super().__init__(request);
        self.projectId = self.request.getParameter("id",acceptNone=True);
class UserViews(AbstractView):
    def __init__(self,request):
        super().__init__(request);
        self.setReaderStratedy(UserParameterReader);
    def register(self):
<<<<<<< HEAD
        #from ou_fyp.services.templates.InputForm import RegisterForm;
=======
        from ou_fyp.services.templates.InputForm import RegisterForm;
>>>>>>> 495fa86ea5d97b89dda4e984fe58b68040564eed
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
                return "OK";
        """
        u = User().objects.create_user(self.parsReader.uname,self.parsReader.email,self.parsReader.pw);
        u.first_name = self.parsReader.fname;
        u.last_name = self.parsReader.lname;
        u.save();
        """
