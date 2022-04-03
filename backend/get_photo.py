def get_upload_to_profile(instance, filename):
    return u'images/%s/%s' % (instance.id, filename)