# Create your views here.
from ou_fyp.libs.RequestDecorate import *;
from ou_fyp.libs.MyExceptions import *;
from django.http import HttpRequest,HttpResponse;
from ou_fyp.libs.ResponseFormats import *;
from ou_fyp.services.AbstractView import *;
def testBFLink(request,bar):
    request = RequestDecorator(request);
    request.addPars("id",bar);
    return handleRequest(request,"test","hellowould","services");
def instanceFactoryMethod(request,handler,service,package):
    if package == "services":
        package = "services"
    elif package == "templates":
        package = "services.templates";
    module = __import__("{}.{}.{}Views".format("ou_fyp",package,handler.capitalize()),fromlist=["{}Views".format(service)]);
    handler = handler.capitalize();
    classInstance = getattr(module,"{}Views".format(handler))(request);
    classInstance.responseFormat = getattr(Formats,request.getParameter("responseFormat","json").upper());
    return classInstance;
def handleRequest(request,handler,service,invokeType):
    try:
        if not isinstance(request,RequestDecorator):
            request = RequestDecorator(request);
        classInstance = instanceFactoryMethod(request,handler,service,invokeType);
        responseContent = classInstance.invoke(service);
        if isinstance(responseContent,HttpResponse):
            return responseContent;
        else:
            if responseContent is None:
                responseContent = classInstance.simpleOutPut();
            if invokeType == "services":
                contentType = "text/html";
                resformat = request.getParameter("responseFormat","json");
                if resformat == Formats.JSON:
                    contentType = "application/json";
                elif resformat == Formats.HTML:
                    pass;
                elif resformat == Formats.XML:
                    contentType = "application/xml";
                else: 
                    raise FormatUnSuportedError(resformat);
                return HttpResponse(responseContent,content_type=contentType);
            else:
                return HttpResponse(responseContent);
    except ImportError as ipe:
        return HttpResponse(ipe);
    except ParameterNotFoundException as pne:
        return HttpResponse(pne);
    except InvokeMethodException as ime:
        return HttpResponse(ime);
    except ForbiddenException as fe:
        return fe.getRemedialAction();

