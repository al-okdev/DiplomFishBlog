def get_upload_to_profile(instance, filename):
    return u'images/%s/%s' % (instance.id, filename)

def get_upload_to_post(instance, filename):
    return u'images/%s/%s' % (instance.id, filename)


def get_upload_to_comment(instance, filename):
    return u'images/%s/%s' % (instance.id, filename)

def get_upload_to_replycomment(instance, filename):
    return u'images/%s/%s' % (instance.id, filename)

def get_upload_to_shop(instance, filename):
    return u'images/%s/%s' % (instance.id, filename)

def get_upload_to_category(instance, filename):
    return u'images/%s/%s' % (instance.id, filename)

def get_upload_to_product(instance, filename):
    return u'images/%s/%s' % (instance.id, filename)