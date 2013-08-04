# Create your views here.
from django.http import HttpResponse
from django.template import Context,Template,loader
from ou_fyp.services.AbstractView import *;
class TestViews(AbstractView):
    def hellowould(self):
        return self.request.getParameter("id");
