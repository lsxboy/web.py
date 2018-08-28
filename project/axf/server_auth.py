from axf.md5_auth import encryption
from axf.models import User

def Server_auth(sessionId,phone):
    sessions = encryption(sessionId)
    try:
        users = User.objects.filter(phoneNum=phone).get(session=sessions)
    except User.DoesNotExist as e:
        return False
    return users

