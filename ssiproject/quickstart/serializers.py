from django.contrib.auth.models import User, Group
from rest_framework import serializers
from quickstart.models import Visit
from rest_framework import permissions

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
		
class VisitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Visit
		fields = ('created','title','code','linenos', 'owner', 'doctor')


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        