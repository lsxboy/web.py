#导入序列化模块
from rest_framework import serializers
from axf.models import *


#创建序列化User的类

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phoneNum','passwd','tokenValue','headImg','integral','vipLevel','createTime','lastLoginTime','isDelete')