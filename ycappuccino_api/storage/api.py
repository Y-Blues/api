#app="all"
from ycappuccino_api.core.api import CFQCN
from ycappuccino_api.proxy.api import YCappuccinoProxy


class IRightSubject(YCappuccinoProxy):
    name = CFQCN.build("IRightSubject")

    def __init__(self):
        """ abstract constructor """
        super().__init__()

    def get_token_subject(self, a_subsystem, a_tenant):
        return {
            'sub': a_subsystem,
            "tid": a_tenant
        }

class IBootStrap(IRightSubject):
    """ Manage bootstrap interface. it allow to initialize for an item data or do a bootstrap operation"""
    name = CFQCN.build("IBootStrap")

    def __init__(self):
        """ abstract constructor """
        super().__init__()



    def bootstrap(self):
        """ method call while manage is initialized and finish to allow to bootstrap operation """
        pass

    def get_id(self):
        pass


class IStorage(YCappuccinoProxy):
    """ interface of proxy component that allow to bind all
    YCappuccino ycappuccino_core component and notify client ipopo of ycappuccino_core component"""
    name = CFQCN.build("IStorage")

    def __init__(self):
        """ abstract constructor """
        super().__init__()


class ITrigger(YCappuccinoProxy):
    """ """
    name = CFQCN.build("ITrigger")

    def __init__(self, a_name, a_item_id, a_actions, a_synchronous=False, a_post=False):
        super().__init__()
        self._synchronous = a_synchronous
        self._post = a_post
        self._name = a_name
        self._item_id = a_item_id
        self._actions = a_actions

    def execute(self, a_action, a_model):
        pass

    def is_synchronous(self):
        return self._synchronous

    def get_item(self):
        return self._item_id

    def get_actions(self):
        return self._actions

    def get_name(self):
        return self._name

    def is_post(self):
        return self._post

    def is_pre(self):
        return not self._post

class IFilter(YCappuccinoProxy):
    """ """
    name = CFQCN.build("IFilter")

    def __init__(self):
        super().__init__()

    def get_filter(self, a_tenant=None):
        pass

class IManager(YCappuccinoProxy):
    """ """
    name = CFQCN.build("IManager")

    def __init__(self):
        super().__init__()


class IDefaultManager(IManager):
    """ """
    name = CFQCN.build("IDefaultManager")

    def __init__(self):
        super().__init__()


class IOrganizationManager(IManager):
    """ """
    name = CFQCN.build("IOrganizationManager")

    def __init__(self):
        super().__init__()

class IUploadManager(IDefaultManager):
    """ """
    name = CFQCN.build("IUploadManager")

    def __init__(self):
        super().__init__()


class IItemManager(IManager):
    """ """
    name = CFQCN.build("IItemManager")

    def __init__(self):
        super(IManager, self).__init__()

