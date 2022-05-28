from storages.backends.s3boto3 import S3Boto3Storage, S3Boto3StorageFile


class ApkStorage(S3Boto3Storage):
    location = 'apk'
    file_overwrite = True
