from ou_fyp.libs.ResponseFormats import *;
class InvokeMethodException(Exception):
    def __init__(self,invokedMethod):
        self.methodName = invokedMethod;
    def __str__(self):
        return "{} is private method!".format(self.methodName);
class AbstractParameterReader:
    def __init__(self,request):
        from ou_fyp.libs.RequestDecorate import RequestDecorator;
        if isinstance(request,RequestDecorator):
            self.request = request;
        else:
            raise TypeError;
class AbstractView:
    def __init__(self,request):
        self.responseFormat=Formats.JSON;
        self.request = request;
        self.setReaderStratedy(AbstractParameterReader);
    def simpleOutPut(self,status="OK",message="Request Successful"):
            basicResult = {"Status":status,"Messages":message};
            if self.responseFormat == Formats.JSON:
                import json;
                return json.JSONEncoder().encode(basicResult);
            elif self.responseFormat == Formats.XML:
                import xml.dom.minidom as xml;
                xml_docs = xml.getDOMImplementation();
                root = xml_docs.createDocument(None,"Result",None);
                for key,value in basicResult.items():
                    root.documentElement.setAttribute(key,value);
                return root.toprettyxml(encoding="utf-8").decode("utf-8");
    def setReaderStratedy(self,stratedyClass):
        self.parsReader= stratedyClass(self.request);
    def invoke(self,service):
        if service.startswith("__") or service.endswith("__") or (service.startswith("__") and service.endswith("__")):
            raise InvokeMethodException(service);
        else:
            self.invokedService = service;
            self.submitLink = "/services/{}/{}".format(self.__class__.__name__.lower()[0:-5],self.invokedService);
            return getattr(self,service)();
"""
class Test(AbstractView):
    def helloWorld(self):
        print(self.request);
    def __test1(self):
        pass;
    def test1__(self):
        pass;
    def __test1__(self):
        pass;
a=Test("HelloWorld");
a.invoke("helloWorld");
#a.invoke("__test1");
#a.invoke("test1__");
#a.invoke("__test1__");
"""
