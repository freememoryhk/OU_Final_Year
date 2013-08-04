from ou_fyp.libs.ResponseFormats import *;
class InvokeMethodException(Exception):
    def __init__(self,invokedMethod):
        self.methodName = invokedMethod;
    def __str__(self):
        return "{} is private method!".format(self.methodName);
class AbstractView:
    def __init__(self,request):
        self.responseFormat=Formats.JSON;
        self.request = request;
    def invoke(self,service):
        if service.startswith("__") or service.endswith("__") or (service.startswith("__") and service.endswith("__")):
            raise InvokeMethodException(service);
        else:
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
