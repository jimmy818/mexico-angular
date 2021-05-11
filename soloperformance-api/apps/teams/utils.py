
from apps.security import models as model_user

def get_user_managers(pk,type):
    from apps.security import serializers as serializers_user
    users = model_user.User.objects.filter(
        institution=pk,
        type=type
        )
    
    serializer = serializers_user.InstitutionUserSerializer(users,many=True)
    
    return serializer.data
    