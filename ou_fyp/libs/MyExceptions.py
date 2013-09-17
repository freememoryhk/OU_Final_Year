class ForbiddenException(Exception):
    def getRemedialAction(self):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied;
class RequestLoginException(ForbiddenException):
    def __init__(self,next,redirect="/user/login"):
        self.currentPage=next;
        self.loginPage=redirect;
    def getRemedialAction(self):
        from django.shortcuts import redirect;
        redirectObj = redirect("{}?next={}".format(self.loginPage,self.currentPage));
        return redirectObj;