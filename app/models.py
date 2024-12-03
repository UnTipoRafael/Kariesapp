from django.db import models
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage


'''
from gdstorage.storage import GoogleDriveStorage, GoogleDrivePermissionType, GoogleDrivePermissionRole, GoogleDriveFilePermission
permission =  GoogleDriveFilePermission(
   GoogleDrivePermissionRole.READER,
   GoogleDrivePermissionType.USER,
   "ser-649@karemapp.iam.gserviceaccount.com"
)
'''
##gd_storage = GoogleDriveStorage(permissions=(permission,),)

gd_storage = GoogleDriveStorage()

class ImagenDrive(models.Model):
   name = models.CharField(max_length=250)
   imagen = models.FileField(upload_to='images/',storage=gd_storage )
   ok = models.FileField(upload_to='predict/', storage=gd_storage)

class ImagenLocal(models.Model):
   name = models.CharField(max_length=250)
   imagen = models.FileField(upload_to='images/')
   ok = models.FileField(upload_to='predict/')
