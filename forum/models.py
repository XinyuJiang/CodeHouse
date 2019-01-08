from django.db import models


# Create your models here.
class Userinfo(models.Model):
    nickname = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    sex = models.CharField(max_length=10, null=True, blank=True)#数据库内可以为空值，并且Django角度插入内容可以是空
    age = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=50,null=True,blank=True)
    email = models.CharField(max_length=50)



class Tiezi(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    category = models.CharField(max_length=50)
    create_time = models.DateField(auto_now_add=True)


class Dongtai(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    content = models.CharField(max_length=300)
    create_time = models.DateField(auto_now_add=True)


class Comment_Tiezi(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    tiezi = models.ForeignKey(Tiezi, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    create_time = models.DateField(auto_now_add=True)


class Comment_Dongtai(models.Model):
    user = models.ForeignKey(Userinfo, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)
    dongtai = models.ForeignKey(Dongtai, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    create_time = models.DateField(auto_now_add=True)

