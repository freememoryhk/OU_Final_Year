class ParameterNotFoundException(Exception):
    def __init__(self,parameters,parameterKey):
        self.parameters = parameters;
        self.keys = parameterKey;
    def __str__(self):
        tableOfAllParameters = "<table border='1'>";
        tableOfAllParameters+= "<tr>";
        tableOfAllParameters+= "<td>";
        tableOfAllParameters+= "Key";
        tableOfAllParameters+= "</td>";
        tableOfAllParameters+= "<td>";
        tableOfAllParameters+= "Value";
        tableOfAllParameters+= "</td>";
        tableOfAllParameters+= "</tr>";
        for key in self.parameters.keys():
            tableOfAllParameters+= "<tr>";
            tableOfAllParameters+= "<td>";
            tableOfAllParameters+= key;
            tableOfAllParameters+= "</td>";
            tableOfAllParameters+= "<td>";
            tableOfAllParameters+= self.parameters.get(key);
            tableOfAllParameters+= "</td>";
            tableOfAllParameters+= "</tr>";
        tableOfAllParameters += "</table>";
        return "{} not found in parameters<br/>Details:<br/>{}".format(self.keys,tableOfAllParameters);
class RequestDecorator:
    def __init__(self,request):
        self.request = request;
        self.pars = self.__getParameters().copy();
    def addPars(self,key,value):
        self.pars.update({key:value});
    def __getParameters(self):
        if self.request.method == "GET":
            return self.request.GET;
        elif self.request.method == "POST":
            return self.request.POST;
    def __onFailureToGetParameter(self,default,key,acceptNone=False):
        if acceptNone:
            return default;
        else:
            if default is not None:
                return default;
            else:
                raise ParameterNotFoundException(self.__getParameters(),key);
    def getParameter(self,parameterKey,default=None,formatter=None,acceptNone=False):
        if self.pars.__contains__(parameterKey):
            value = self.pars.get(parameterKey);
            if len(value.strip()) < 1:
                return self.__onFailureToGetParameter(default=default,key=parameterKey,acceptNone=acceptNone);
            else:
                if formatter is None:
                    return self.pars.get(parameterKey);
                else:
                    return formatter.format(self.pars.get(parameterKey));
        else:
            return self.__onFailureToGetParameter(default=default,key=parameterKey,acceptNone=acceptNone);
