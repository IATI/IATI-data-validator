import time
import requests
import os

api = "http://localhost:3000"

while True:

    r = requests.get(api + '/internal/file/next')

    if r.status != 200:
        time.sleep(10)
        continue

    iatiFileData = r.json()

    r = requests.get(iatiFileData.fileUrl)

    if r.status != 200:
        payload = {id: iatiFileData._id, error: "DOWNLOAD"}
        requests.post(api + '/internal/file/report', payload)
        continue

    os.system('ant -f build-engine.xml -Dfilemask=' + iatiFileData._id + ' feedback')
    os.system('ant -f build-engine.xml -Dfilemask=' + iatiFileData._id + ' json')

    #All the magical knowledge of the paths of the files produced by the commands above is a hangover from the D4D v1

    with open('/work/space/json/' + iatiFileData._id + '.json', 'rb') as f:
         r = requests.post(api + '/internal/file/report', files={iatiFileData._id + 'json': f})
    
    os.remove('/work/space/dest/$ID.feedback.xml')
    os.remove('/work/space/json/$ID.json')