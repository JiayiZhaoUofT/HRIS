from app.file_processing import find_email,find_phone,judge_skills
from app.getUuid import g_uid
from app.candidateDDB import putCandidateItem

def createNewCandidate(managerID, positionID,fileobj, addOnS3, skillset):
    email = find_email(fileobj)
    phone = find_phone(fileobj)
    skills = judge_skills(fileobj, skillset)
    resumeAddr = addOnS3
    candidateID = g_uid()
    putCandidateItem(managerID, positionID, candidateID, email, phone, skills, resumeAddr)
    print(email)
    print(phone)
