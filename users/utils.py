
def user_upload_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.users.id, filename)

def property_upload_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.users.id, filename )