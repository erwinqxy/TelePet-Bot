from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from apiclient.http import MediaFileUpload

import cv2
import urllib.request
import numpy as np

SCOPES = ['https://www.googleapis.com/auth/drive']
KEY_FILE_LOCATION = 'telepet-bot-337612-f2f9ebccf500.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
            KEY_FILE_LOCATION, scopes=SCOPES)

# https://developers.google.com/drive/api/v3/quickstart/python
service = build('drive', 'v3', credentials=credentials)

def change_sharing_permission_link(file_id):
    request_body = {
        'role': 'reader',
        'type': 'anyone'

    }

    response_permission = service.permissions().create(
        fileId=file_id,
        body=request_body
    ).execute()

    #print('response_permission:',response_permission)

def url_to_image(url):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
	# return the image
	return image
'''
folder_id = "1WyWunkPQMpQPe_3faZFXdwkdq0ayjRk3" #images folder
image_path = "computer_vision/cv-images/trump-face.png"
image_name = str(image_path.split('/')[-1])
'''
def write_image_to_gdrive(folder_id,image_path,image_name):
    file_metadata = {
        'name': image_name,
        #'parents': [cloudFolder['id']]
        'parents': [folder_id]
    }

    query = "'{}' in parents".format(folder_id)
    filesInFolder = service.files().list(q=query, orderBy='folder', pageSize=10).execute()
    items = filesInFolder.get('files', [])

    # if no images 
    if not items:
        print(f'No files found, adding image {image_name} to images folder')
        media = MediaFileUpload(image_path, mimetype='image/png')
        # https://developers.google.com/drive/v3/web/manage-uploads
        cloudFile = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields='id').execute()
        #print('File ID: %s' % cloudFile.get('id'))

    # images present
    else:
        #print('Files:')
        print('files found')
        for item in items:
            #print('{0} ({1})'.format(item['name'], item['id']))
            
            if item['name'] == str(image_path.split('/')[-1]):
                print(f'{image_name} exists in folder, deleting existing image')
                service.files().delete(fileId=item['id']).execute()

            print(f'adding {image_name} image to images folder')
            media = MediaFileUpload(image_path, mimetype='image/png')
            # https://developers.google.com/drive/v3/web/manage-uploads
            cloudFile = service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()
            #print('File ID: %s' % cloudFile.get('id'))
            
            # service.files().delete(fileId=item['id']).execute()  # Optional cleanup
        
        
        # Update Sharing Setting
        file_id = cloudFile.get('id')
        
        change_sharing_permission_link(file_id)
        
        '''
        # Print Sharing URL
        response_share_link = service.files().get(
            fileId=file_id,
            fields='webViewLink'
        ).execute()
        print('response_share_link:',response_share_link['webViewLink'])
        '''

'''
write_image_to_gdrive(folder_id,image_path,image_name)
#image_url = response_share_link['webViewLink']
image_url = "https://drive.google.com/uc?id="+str(file_id)
np_image = url_to_image(image_url)

cv2.imwrite(f'computer_vision/cv-images/google_drive_downloaded.png',np_image)
'''

# List files in our folder
# https://developers.google.com/drive/v3/web/search-parameters
# https://developers.google.com/drive/v3/reference/files/list

'''
query = "'{}' in parents".format(folder_id)
filesInFolder = service.files().list(q=query, orderBy='folder', pageSize=10).execute()
items = filesInFolder.get('files', [])

# Print the paged results
if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print('{0} ({1})'.format(item['name'], item['id']))
        # service.files().delete(fileId=item['id']).execute()  # Optional cleanup
'''



# Call the Drive v3 API
'''
results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))
'''
#print(service)

'''
def createFolder(name):
    folder_id = "1WyWunkPQMpQPe_3faZFXdwkdq0ayjRk3"
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id]
    }    
    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    print('Folder ID: %s' % file.get('id'))
    return file

cloudFolder = createFolder('folder_name')

file_metadata = {
    'name': 'text file',
    #'parents': [cloudFolder['id']]
    'parents': [cloudFolder['id']]
}

with open("computer_vision/text.txt","r") as file:
    
    # https://developers.google.com/api-client-library/python/guide/media_upload
    media = MediaFileUpload(file.name, mimetype='text/plain')
    # https://developers.google.com/drive/v3/web/manage-uploads
    cloudFile = service.files().create(body=file_metadata).execute()
'''


'''
folder_metadata = {
    'name': 'My Test Folder',
    'mimeType': 'application/vnd.google-apps.folder'
}
cloudFolder = service.files().create(body=folder_metadata).execute()

# Upload a file in the folder
# https://developers.google.com/api-client-library/python/guide/media_upload
# https://developers.google.com/drive/v3/reference/files/create

file_metadata = {
    'name': 'A Test File',
    'parents': [cloudFolder['id']]
}

with open("computer_vision/text.txt","r") as file:
    
    # https://developers.google.com/api-client-library/python/guide/media_upload
    media = MediaFileUpload(file.name, mimetype='text/plain')
    # https://developers.google.com/drive/v3/web/manage-uploads
    cloudFile = service.files().create(body=file_metadata).execute()


userEmail = "telepetbot@gmail.com"
# Share file with a human user
# https://developers.google.com/drive/v3/web/manage-sharing
# https://developers.google.com/drive/v3/reference/permissions/create

cloudPermissions = service.permissions().create(fileId=cloudFile['id'], 
    body={'type': 'user', 'role': 'reader', 'emailAddress': userEmail}).execute()

cp = service.permissions().list(fileId=cloudFile['id']).execute()
print(cp)
'''
'''
with open("computer_vision/cv-images/trump-face.png","r") as file:
    #do something here with file
    file_drive = service.CreateFile({'title':os.path.basename(file.name) })  
    file_drive.SetContentString(file.read()) 
    file_drive.Upload()
'''