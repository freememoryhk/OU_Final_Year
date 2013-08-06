from django.core.paginator import Paginator;

class ResponseDBTableConventer:
    page =1;
    perPageSize = 15;
    def __init__(self,model,page=1,order=None):
        self.model = model;
        self.page = page;
        if order is None:
            self.order = self.model._meta.pk.name;
        else:
            self.order = order;
    def getPaginator(self):
        self.getResult();
        return Paginator(self.result,self.perPageSize);
    def getResult(self):
        if not hasattr(self,"result"):
            self.result = self.model.objects.order_by(self.order);
        else:
            return self.result;
    def serialize(self,format,additionalBtn=None):
        result = self.getPaginator().page(self.page);
        from ou_fyp.libs.ResponseFormats import Formats;
        if format == Formats.HTML:
            tableHtml="";
            start=1;
            for row in result:
                if start % 2 ==0 :
                    tableHtml+="<tr>";
                else:
                    tableHtml+="<tr class='odd'>";
                for field in self.model._meta.fields:
                    value=getattr(row,field.name);
                    from django.db import models
                    if isinstance(value,models.Model):
                        tableHtml+="<td>"+value.getDisplay()+"</td>";
                    else:
                        tableHtml+="<td>"+str(value)+"</td>";
                if additionalBtn is not None:
                    for item in additionalBtn:
                        tableHtml+="<td><button id='id_{}_{}' onclick='return row_{}_click(\"{}\")'> {}</button></td>".format(getattr(row,self.model._meta.pk.name),str(item),str.lower(item),getattr(row,self.model._meta.pk.name),str(item));
                tableHtml+="</tr>";
                start+=1;
            return tableHtml;
        else:
            from django.core import serializers;
            return serializers.serialize(format,result);
