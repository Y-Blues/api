'''

Core api description

@author: apisu
'''
import logging


class CFQCN(object):
    """
    CFQCN class : Ful Qualified Class Name
    """
    @staticmethod
    def build(aClassName):
        wFQCN =  '.'.join(["ycappuccino_storage.api",aClassName])
        wLog = logging.getLogger(__name__)
        wLog.info("FQCN '{0}' ...".format(wFQCN))
        return wFQCN


class IActivityLogger(object):
    """ Activity logger of the application. admit a property name that identified the logger"""
    name = CFQCN.build("IActivityLogger")

    def __init__(self):
        """ abstract constructor """



class IConfiguration(object):
    """ interface of configuration service"""
    name = CFQCN.build("IConfiguration")

    def __init__(self):
        """ abstract constructor """
        pass


class YCappuccino(object):
    """ interface of YCappuccino component """
    name = CFQCN.build("YCappuccino")

    def __init__(self):
        """ abstract constructor """
        self._id = None

    def id(self):
        return self._id

class IListComponent(object):
    """ interface of YCappuccino component that list of YCappuccino component """
    name = CFQCN.build("IListComponent")

    def __init__(self):
        """ abstract constructor """
        pass

class IServerProxy(object):
    """ interface of the service endpoint that list proxy """
    name = CFQCN.build("IServerProxy")

    def __init__(self):
        """ abstract constructor """
        pass



class IService(object):
    """ interface that describe a service  """
    name = CFQCN.build("IService")

    def __init__(self):
        pass

    def is_sercure(self):
        return True

    def has_post(self):
        return True

    def has_put(self):
        return False

    def has_get(self):
        return False

    def has_delete(self):
        return False

    def has_root_path(self):
        return True

    def get_name(self):
        pass

    def get_extra_path(self):
        """ return the list of extra path that are manage by service """
        return {
            "post":[],
            "get": [],
            "put": [],
            "delete": []
        }

    def post(self, a_header, a_url_path, a_body):
        pass

    def put(self, a_header, a_url_path, a_body):
        pass

    def get(self, a_header, a_url_path):
        pass

    def delete(self, a_header, a_url_path):
        pass



