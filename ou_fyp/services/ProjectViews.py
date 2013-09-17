# Create your views here.
from django.http import HttpResponse
from django.template import Template,loader
from django.template import RequestContext as Context
from ou_fyp.services.AbstractView import *;
from ou_fyp.services.templates.InputForm import *;
from django.contrib.auth.models import User,Group;
#from django.core.context_processors import csrf;
from ou_fyp.models import *;
class ProjectParameterReader(AbstractParameterReader):
    def __init__(self,request):
        super().__init__(request);
        self.projectId = self.request.getParameter("id",acceptNone=True);
class ProjectViews(AbstractView):
    def __init__(self,request):
        super().__init__(request);
        self.setReaderStratedy(ProjectParameterReader);
    """
    def show(self):
        uf = RegisterForm();
        templateObj = loader.get_template("register.html");
        #fill = dict(list(csrf(self.request.request).items())+list({"form":uf,"title":"Register to system","submitLink":self.submitLink}.items()))
        fill = {"form":uf,"noajax":True,"title":"Register to system","submitLink":self.submitLink};
        context= Context(self.request.request,fill);
        return templateObj.render(context);    
    """
    """
    def load(self):
        import io;
        out = io.BytesIO(contentObj.project_content);
        out.flush();
        out.seek(0);
        from django.core.servers.basehttp import FileWrapper;
        response = HttpResponse(FileWrapper(out),content_type='text/plain');
        response['Content-Disposition'] = 'attachment; filename=prueba.txt';
        return response;
    """
    def create(self):
        self.checkLogedIn();
        pc = CreateProjectForm(self.request.request.POST,self.request.request.FILES);
        if pc.is_valid():
            submitData = pc.cleaned_data;
            projectObj = pc.save(commit=False);
            projectObj.designer = self.request.request.user;
            projectObj.save();
            contentObj = ProjectContentLog();
            contentObj.project=projectObj;
            contentObj.commit_user=self.request.request.user;
            contentObj.change_message="Initial";
            contentObj.project_content=submitData["project_contents"];
            contentObj.project_version="0";
            contentObj.save();
            for tag in submitData["project_tags"]:
                tagObj = None;
                if not TagsProxy.objects.filter(tag_name=tag).exists():
                    tagObj = TagsProxy();
                    tagObj.tag_name = tag;
                    tagObj.save();
                else:
                    tagObj = TagsProxy.objects.get(tag_name=tag);
                tagObj.hit();
                projectObj.project_tags.add(tagObj);
            projectObj.project_tags.create();
        else:
            return "Error:{0}".format(pc.errors);
