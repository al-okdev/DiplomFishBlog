def get_upload_to_profile(instance, filename):
    return u'images/%s/%s' % (instance.id, filename)

def get_upload_to_post(instance, filename):
    return u'images/%s/%s' % (instance.id, filename)