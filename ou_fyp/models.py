from django.db import models
from django.contrib.auth.models import User,Group;
class AutoZeroField(models.AutoField,metaclass=models.SubfieldBase):
    description = "Let auto increment with zero fill";
    def to_python(self,value):
        from ou_fyp.libs.Formatter import NumericZeroFormatter;
        if value is None:
            return super(AutoZeroField,self).to_python(value); 
        else:
            return NumericZeroFormatter().format(str(value));
class AbstractBaseModel(models.Model):
    #id=AutoZeroField(primary_key=True);
    def __combinManyKeyInToOneKey(self,keys):
        combinedKey="";
        for key in keys:
            combinedKey+=str(key)+"_";
        return combinedKey[0:len(combinedKey)-1];
    class Meta:
        abstract = True;
class Tags(AbstractBaseModel):
    tag_id = AutoZeroField(primary_key=True);
    tag_name = models.CharField(max_length=25,unique=True);
    tag_hit_counts = models.IntegerField(default=0);
class TagsProxy(Tags):
    def hit(self):
        if self.tag_id is not None:
            self.tag_hit_counts+=1;
            self.save();
    def popluarTagsList(self):
        popluarTagsLists = Tags.objects.all().order_by("-tag_hit_counts")[0:10];
        popluarTagsTuple = [];
        for tags in popluarTagsLists:
            popluarTagsTuple.append((tags.tag_id,tags.tag_name));
        return popluarTagsTuple;
    def excludePopluarTagsList(self,popluarTagsTuple = None):
        popluarTagsLists = [];
        if popluarTagsTuple is None:
            popluarTagsTuple = self.popluarTagsLists();
        for tags in popluarTagsTuple:
            popluarTagsLists.append(tags[0]);
        otherList = Tags.objects.filter(~models.Q(tag_id__in=popluarTagsLists));
        return otherList;
    class Meta:
        proxy = True;
class ThreeDimensionsProjects(AbstractBaseModel):
    project_id = AutoZeroField(primary_key=True,max_length=11);
    designer = models.ForeignKey(User,db_index=True);
    price = models.DecimalField(max_digits=7,decimal_places=1,default=0.0);
    project_description = models.TextField(max_length=255);
    #project_tags = AutoZeroManyToManyField(Tags,through="Threedimensionsprojects_tags");
    project_tags = models.ManyToManyField(Tags);
    project_shared_group = models.ManyToManyField(Group);
"""
class Threedimensionsprojects_tags(AbstractBaseModel):
    tag = AutoZeroForeignKey(Tags);
    project = AutoZeroForeignKey(ThreeDimensionsProjects);
"""
class PurchasedProjects(AbstractBaseModel):
    deal_date = models.DateTimeField(auto_now_add=True,editable=False);
    buyer = models.ForeignKey(User,db_index=True)
    project = models.ForeignKey(ThreeDimensionsProjects,db_index=True);
    price = models.DecimalField(max_digits=7,decimal_places=1,default=0.0);
    trading_id = models.CharField(primary_key=True,max_length=23);
    def save(self,*args,**kwargs):
        self.trading_id = self.__combinManyKeyInToOneKey([self.project.project_id,self.buyer.id]);
        super(PurchasedProjects,self).save(*args,**kwargs);
class ProjectContentLog(AbstractBaseModel):
    project = models.ForeignKey(ThreeDimensionsProjects,db_index=True);
    commit_user =models.ForeignKey(User,db_index=True);
    change_message = models.TextField(max_length=255,blank=True);
    change_time = models.DateTimeField(auto_now_add=True,editable=False);
    from django import forms;
    import base64;
    _project_content = models.TextField(max_length=1*1024*1024*1024*8,db_column="project_content");
    def set_content(self,submitFile):
        bufferStorage = bytearray();
        for byte in submitFile.chunks():
            bufferStorage.append(byte);
        self._project_content = base64.encodebytes(bufferStorage).encode("ascii");
    def get_content(self,encodingFile):
        return base64.decodebytes(self._project_content.decode("ascii"));
    project_content=property(get_content,set_content);
    project_version = models.CharField(max_length=10);
    project_version_id = models.CharField(primary_key=True,max_length=80);
    project_import = models.ManyToManyField('self');
    def save(self,*args,**kwargs):
        self.project_version_id = self.__combinManyKeyInToOneKey([self.project.project_id,self.change_time]);
        super(ProjectContentLog,self).save(*args,**kwargs);
