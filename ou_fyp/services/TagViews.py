# Create your views here.
from django.http import HttpResponse
from django.template import Template,loader
from django.template import RequestContext as Context
from ou_fyp.services.AbstractView import *;
from ou_fyp.services.templates.InputForm import *;
from django.contrib.auth.models import User,Group;
#from django.core.context_processors import csrf;
class TagParameterReader(AbstractParameterReader):
    def __init__(self,request):
        super().__init__(request);
        self.projectId = self.request.getParameter("id",acceptNone=True);
class TagViews(AbstractView):
    def __init__(self,request):
        super().__init__(request);
        self.setReaderStratedy(TagParameterReader);
    def create(self):
        tc = TagsCreateForm(self.request.request.POST);
        if tc.is_valid():
            t = tc.save();
            if not self.request.request.is_ajax():
                return self.simpleOutPut();
            else:
                return self.simpleOutPut(status="Failure");
