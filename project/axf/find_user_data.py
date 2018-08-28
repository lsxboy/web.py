import re

def find_user_data(data):
    matchObj = re.findall(r"('.*?')", str(data), re.M | re.I)
    if matchObj:
        mail = matchObj[1].replace("'", "")
        userid = matchObj[3].replace("'", "")
        return userid, mail
    else:
        return None