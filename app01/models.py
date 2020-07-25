from django.db import models

# Create your models here.
class Publisher(models.Model):
    name = models.CharField(max_length=32)

class Book(models.Model):
    name = models.CharField(max_length=32)
    # publisher = models.ForeignKey(Publisher)
    # models.CASCADE 为级联删除
    # models.PROTECT 保护
    # models.SET(val) # 删除后设置为指定值
    # models.SETDEFAULT, default=val  删除后设置为default值
    # model.SET_NULL 删除后设置为null
    publisher = models.ForeignKey("Publisher", on_delete=models.CASCADE)  # 默认是级联删除
