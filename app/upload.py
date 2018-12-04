from flask import render_template, request, flash, redirect,url_for
from app import webapp
import os
from app.S3UploadDownload import s3_upload,s3_download
from app.file_processing import find_email,find_phone,judge_skills
from app.createNewCandidate import createNewCandidate
from app.jobDDB import query_skills
import boto3
# bucketName = "a3-resume"
bucketName = "a3-resume"

@webapp.route('/dev5/upload_submit/<mID>/<pID>',methods=['POST'])
@webapp.route('/upload_submit/<mID>/<pID>',methods=['POST'])
def upload_submit(mID, pID):
    file = request.files['resume']
    f = file.read()
    filename = ''.join(e for e in file.filename if e.isalnum())
    location = s3_upload(bucketName, f, filename)
    # managerID = mID
    positionID = pID
    managerID = "43601e88-f2ab-11e8-ba53-f40f242190e7"
    skills = query_skills(positionID)
    if not skills:
        skills = ""
    else:
        skills = skills[0]['skills']

    createNewCandidate(managerID=managerID,
                       positionID=positionID,
                       fileobj=file,
                       addOnS3=location,
                       skillset=skills)

    return redirect(url_for('displayPosition'))



#
# @webapp.route('/',methods=['GET'])
# @webapp.route('/index',methods=['GET'])
# @webapp.route('/upload',methods=['GET'])
# def upload():
#     return render_template("/upload.html")
#
# @webapp.route('/skill_check',methods=['POST'])
# def upload_and_skill_check():
#     if not request.files:
#         return render_template("/upload.html", error = "Please select a file!")
#     file = request.files['resume']
#     filepath = os.path.join('static', file.filename)
#     file.save(filepath)
#     location = s3_upload(filepath, bucketName, file.filename)
#     # print(msg)
#     managerID = "36aa0c66-f2ca-11e8-9e85-f40f242190e7"
#     positionID = "be9aa298-f2c2-11e8-a4d7-f40f242190e7"
#     skills = query_skills(positionID)
#     createNewCandidate(managerID=managerID,
#                        positionID=positionID,
#                        filepath=filepath,
#                        addOnS3=location,
#                        skillset=skills)
#
#     return render_template("/skillCheck.html")

