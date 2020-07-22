import time
import requests
import os
import json
import hashlib

api = "http://localhost:3000"

while True:
    try:
        r = requests.get(api + '/internal/file/next')
    except:
        time.sleep(10)
        continue

    if r.status_code != 200:
        time.sleep(10)
        continue

    iatiFileData = r.json()

    r = requests.get(iatiFileData.fileUrl)

    if r.status != 200:
        payload = {id: iatiFileData._id, error: "DOWNLOAD"}
        requests.post(api + '/internal/file/report', payload)
        continue

    iatiFileData['fileMD5'] = hashlib.md5(r.content.encode('utf-8')).hexdigest()
 
    with open('/work/space/input/' + iatiFileData.fileMD5 +'.xml, 'wb') as f:
        f.write(r.content)

    os.system('ant -f build-engine.xml -Dfilemask=' + iatiFileData.fileMD5 + ' feedback')
    os.system('ant -f build-engine.xml -Dfilemask=' + iatiFileData.fileMD5 + ' json')

    #All the magical knowledge of the paths of the files produced by the commands above is a hangover from the D4D v1

    with open('/work/space/json/' + iatiFileData.fileMD5 + '.json', 'rb') as f:
        iatiFileData['validationReport'] = json.load(f)
    
    r = requests.post(api + '/internal/file/report', iatiFileData)
    
    os.remove('/work/space/dest/' + iatiFileData.fileMD5 + '.feedback.xml')
    os.remove('/work/space/json/' + iatiFileData.fileMD5 + '.json')