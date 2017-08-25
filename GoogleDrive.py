from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import httplib2
import os
import re


class GoogleDrive:
    def __init__(self):
        self.scope = "https://www.googleapis.com/auth/drive"
        self.client_secret_file = "client_secret_54.json"
        self.client_name = "Arif Rahman"
        self.credential_file = "token.json"
        self.service = None
        self.all_file_list = []
        self.file_list = []
        self.folder_list = []
        self.http = httplib2.Http()
        store = Storage(os.path.join('', self.credential_file))
        self.credential = store.get()
        if not self.credential or self.credential.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file, self.scope)
            flow.user_agent = self.client_name
            self.credential = tools.run_flow(flow, store, None)

        self.http = self.credential.authorize(self.http)
        self.service = discovery.build("drive", "v3", http=self.http)
        self.list_files()
        self.print_files(False)
        self.print_folders(False)
        return

    def get_scope(self):
        return self.scope

    def get_credential_file_name(self):
        return self.credential_file

    def list_files(self):
        self.all_file_list=[]
        results = self.service.files().list().execute()
        files = results.get("files", [])
        for file in files:
            self.all_file_list.append((file['name'], file['id'], file['mimeType']))

        return

    def print_files(self,print_=True):
        self.file_list=[]
        position = 0;
        for tuple in self.all_file_list:
            if tuple[2] != 'application/vnd.google-apps.folder':
                if print_:
                    print(str(position) + ":" + tuple[0])
                self.file_list.append(tuple)
                position += 1
        return

    def print_folders(self,print_=True):
        self.folder_list=[]
        position = 0;
        for tuple in self.all_file_list:
            if tuple[2] == 'application/vnd.google-apps.folder':
                if print_:
                    print(str(position) + ":" + tuple[0])
                self.folder_list.append(tuple)
                position += 1
        return

    def create_file(self, name, mimeType, parents=[]):
        file_meta_data = dict()
        file_meta_data['name'] = name
        file_meta_data['mimeType'] = mimeType
        file_meta_data['parents'] = parents
        file = self.service.files().create(body=file_meta_data).execute()
        if file['name'] == name:
            print("File Successfully Created")
        else:
            print("Failed To Create File")
        return

    def delete_file(self, index):
        fileId = self.file_list[index][1]
        self.service.files().delete(fileId=fileId).execute()
        print("File Deleted Successfully")
        return

    def delete_folder(self, index):
        fileId = self.folder_list[index][1]
        self.service.files().delete(fileId=fileId).execute()
        print("Folder Deleted Successfully")
        return

    def download_file(self, index):
        fileId = self.file_list[index][1];
        file_name = self.file_list[index][0];
        print("Downloading...",file_name)
        resource = self.service.files().get_media(fileId=fileId)
        download = MediaIoBaseDownload(open(file_name, "wb"), resource)
        done = False

        while done == False:
            status, done = download.next_chunk()
            print("Progress : ", status.progress() * 100)

        return

    def upload_file(self, local_file_name, mimeType, parents=[]):
        file_meta_data = dict()
        file_meta_data['name'] = local_file_name
        file_meta_data['mimeType'] = mimeType
        file_meta_data['parents'] = parents
        if os.path.exists(os.path.join(os.getcwd(), local_file_name)) or os.path.exists(os.path.join('', local_file_name)):
            media = MediaFileUpload(local_file_name, mimeType)
            file = self.service.files().create(body=file_meta_data, media_body=media).execute()
            if file['name'] == local_file_name:
                print("File Successfully Created")
            else:
                print("Failed To Create File")

        else:
            print("File Doesn't Exist Upload Not Possible")
        return


drive = GoogleDrive()


def listFiles():
    drive.list_files()
    print("\nFolders : \n")
    drive.print_folders()
    print("\nFiles : \n")
    drive.print_files()


def deleteFile():
    index = input("insert index for deleting file :")
    if re.match("\d{1,}", str(index)):
        drive.delete_file(int(index))


def uploadFile():
    file_name = input("Enter File Name For uploading :")
    if os.path.exists(os.path.join(os.getcwd(), file_name)) or os.path.exists(os.path.join('', file_name)):
        file_mime_type = input("Enter File mimeType For uploading :")
        parents=[]
        try:
            choice=input("Would You Like To Select Parent(Y/N):")
            choice=choice.lower()
            if choice.strip()=='y':
                folder_index=input("Enter Parent Folder Index :")
                id_num=drive.folder_list[int(folder_index)][1]
                parents=[id_num]
            else:
                print("Mismatch")
               
        except Exception as e:
            print("What hell is happening",e)
        drive.upload_file(file_name, mimeType=file_mime_type,parents=parents)


def downloadFile():
    index = input("insert index for downloading file :")
    if re.match("\d{1,}", str(index)):
        drive.download_file(int(index))
        
        
def finish():
    exit(0)

list = list()
list.append(listFiles)
list.append(deleteFile)
list.append(uploadFile)
list.append(downloadFile)
while True:
 try:
    print(
        "choose your option(every string input should be enclosed with quotation mark) :\n\t0 ) For Listing Files\n\t1 ) For Deleting Files\n\t2 ) Uploading Files\n\t3 ) For Downlaoding Files")
    index = input("Your Choice :")
   
    if re.match("\d{1,}", str(index))>0 and int(index) < 4:
        list[int(index)]()
    else:
        print("Finished")
        finish()

 except Exception as e:
    print("Finished",e)
    finish()
