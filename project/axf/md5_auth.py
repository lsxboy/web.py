import hashlib
def encryption(password):
    md_5 = hashlib.md5()
    md_5.update(password.encode('utf-8'))
    return md_5.hexdigest()

# def login(password):
#     user_session = encryption(password)
#     md5加密session生成密码作为该session的id
    # sessionId = encryption(user_session)



