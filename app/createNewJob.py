from app.jobDDB import putJobItem
from app.getUuid import g_uid

def createNJ(mid,jobtitle,skills):
    msg = putJobItem(mid, g_uid(), jobtitle, skills)
    return msg