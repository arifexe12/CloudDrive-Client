from dropbox.files import *
import dropbox.files
import os
import webbrowser
import re


class DropBox:
    def __init__(self):
        self.access_token=None;
        if os.path.exists(os.path.join('','access_token.txt')):
            f=open("access_token.txt",'r')
            self.access_token=f.read()
            f.close()
        else:
            auth = dropbox.DropboxOAuth2FlowNoRedirect('64jd0opas1s606t', 'wkfv40rkh8u8ju7')
            url = auth.start()
            print("please visit this link and click allow: ", url);
            webbrowser.open(url)
            code = input("Insert Copied Code :")
            self.access_token = auth.finish(code).access_token;
            file = open("access_token.txt", 'w')
            file.write(self.access_token)
            file.close()
        self.dbx = None
        self.dbx = dropbox.Dropbox(self.access_token)

    def list_files(self):
        for name in self.dbx.files_list_folder("", recursive=True).entries:
            if isinstance(name, FileMetadata):
                print("Files :", name.path_lower)
            elif isinstance(name, FolderMetadata):
                print("Folder :", name.path_lower)

    def download_file(self, file_name):
        meta, res = self.dbx.files_download(file_name)
        file = open(meta.name, "wb")
        file.write(res.content)
        file.close()
        print("File Downloaded Successfully")

    def uploead_file(self, local_file_name, drive_path):
        file = open(local_file_name, 'rb')
        bytes=file.read()
        file.close()
        self.dbx.files_upload(bytes, drive_path)
        if self.dbx.files_get_metadata(drive_path)==drive_path:
            print("File Uploaded Successfully")
        else:
            print("Failed To Upload File")

    def delete_file(self,file_path):
        self.dbx.files_delete(file_path)
        print("file deleted successfully")

    def create_folder(self, path_name_including_full_folder_name):
        self.dbx.files_create_folder(path_name_including_full_folder_name)
        if self.dbx.files_get_metadata(path_name_including_full_folder_name).name==path_name_including_full_folder_name:
            print("Folder Created Successfully")
        else:
            print("Failed To Create Folder")


drive = DropBox()


def listFiles():
    drive.list_files()



def deleteFile():
    path = input("insert full path for deleting file :")
    drive.delete_file(path)


def uploadFile():
    file_name = input("Enter File Name For uploading :")
    if os.path.exists(os.path.join('', file_name)):
        path = input("Enter Drive File Path For uploading :")
        drive.upload_file(file_name, path)


def downloadFile():
    drive_path= input("insert file path for downloading file :")
    drive.download_file(drive_path)
    
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
        "choose your option(every string input should be enclosed with quotation mark) :\n0 ) For Listing Files\n1 ) For Deleting Files\n2 ) Uploading Files\n3 ) For Downlaoding Files")
    index = input("Your Choice :")
    if re.match("\d{1,}", str(index)) and int(index) < 4:
        list[int(index)]()
    else:
        print("Finished")
        finish()

 except Exception as e:
    print(e)
    finish()
