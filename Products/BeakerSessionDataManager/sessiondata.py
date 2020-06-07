import time
from six.moves import UserDict

from zope.interface import implementer

from AccessControl.SecurityInfo import ClassSecurityInfo
from Acquisition import Implicit
from App.class_init import InitializeClass
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from ZPublisher.BeforeTraverse import registerBeforeTraverse
from ZPublisher.BeforeTraverse import unregisterBeforeTraverse

from Products.Sessions.interfaces import ISessionDataManager
from Products.Sessions.SessionPermissions import ACCESS_CONTENTS_PERM
from Products.Sessions.SessionPermissions import ACCESS_SESSIONDATA_PERM
from Products.Sessions.SessionPermissions import ARBITRARY_SESSIONDATA_PERM
from Products.Sessions.SessionDataManager import SessionDataManagerErr
from Products.Sessions.SessionDataManager import SessionDataManagerTraverser

from Products.BeakerSessionDataManager.interfaces import ISessionDataObject
from collective.beaker.interfaces import ISession


@implementer(ISessionDataManager)
class BeakerSessionDataManager(SimpleItem, PropertyManager):
    """ Implement a session data manager which uses Beaker sessions.
    """

    security = ClassSecurityInfo()

    ok = {'meta_type':1, 'id':1, 'title': 1, 'icon':1,
          'bobobase_modification_time':1, 'title_or_id':1 }
    security.setDefaultAccess(ok)

    def __init__(self, title=''):
        self.title = title

    #
    #   ZMI
    #

    meta_type = 'Beaker Session Data Manager'
    _requestSessionName = 'SESSION'

    _properties=(
        {'id':'title', 'type':'string', 'mode':'w', 'label':'Title'},
        )

    manage_options = (PropertyManager.manage_options
                    + SimpleItem.manage_options
                     )

    def _session(self):
        """ Here's the core logic which looks up the Beaker session. """
        session = ISession(self.REQUEST)
        return BeakerSessionDataObject(session)

    #
    #   ISessionDataManager implementation
    #
    
    security.declareProtected(ACCESS_SESSIONDATA_PERM, 'getSessionData')
    def getSessionData(self, create=1):
        """ """
        return self._session()
    
    security.declareProtected(ACCESS_SESSIONDATA_PERM, 'hasSessionData')
    def hasSessionData(self):
        """ """
        return True

    security.declareProtected(ARBITRARY_SESSIONDATA_PERM,'getSessionDataByKey')
    def getSessionDataByKey(self, key):
        raise SessionDataManagerErr(
            'Beaker session data manager does not support retrieving arbitrary sessions.'
            )

    security.declareProtected(ACCESS_CONTENTS_PERM, 'getBrowserIdManager')
    def getBrowserIdManager(self):
        """ """
        raise SessionDataManagerErr(
            'Beaker session data manager does not support browser id managers.'
            )

    # Traversal hook

    def manage_afterAdd(self, item, container):
        """ Add our traversal hook """
        self.updateTraversalData(self._requestSessionName)

    def manage_beforeDelete(self, item, container):
        """ Clean up on delete """
        self.updateTraversalData(None)

    def updateTraversalData(self, requestSessionName=None):
        # Note this can't be called directly at add -- manage_afterAdd will
        # work though.
        parent = self.aq_inner.aq_parent

        if getattr(self,'_hasTraversalHook', None):
            unregisterBeforeTraverse(parent, 'BeakerSessionDataManager')
            del self._hasTraversalHook
            self._requestSessionName = None

        if requestSessionName:
            hook = SessionDataManagerTraverser(requestSessionName, self.id)
            registerBeforeTraverse(parent, hook, 'BeakerSessionDataManager', 50)
            self._hasTraversalHook = 1
            self._requestSessionName = requestSessionName

InitializeClass(BeakerSessionDataManager)


def addBeakerSessionDataManager(dispatcher, id, title='', REQUEST=None):
    """ Add a BSDM to dispatcher.
    """
    sdc = BeakerSessionDataManager(title=title)
    sdc._setId(id)
    dispatcher._setObject(id, sdc)
    if REQUEST is not None: # pragma: no cover
        REQUEST['RESPONSE'].redirect('%s/manage_workspace'
                                     % dispatcher.absolute_url())

addBeakerSessionDataManagerForm = PageTemplateFile('www/add_sdm.pt',
                                                     globals())


def session_mutator(func):
    """ Decorator to make a UserDict mutator save the session. """
    def mutating_func(self, *args, **kw):
        res = func(self, *args, **kw)
        self.data.save()
        return res
    return mutating_func


@implementer(ISessionDataObject)
class BeakerSessionDataObject(Implicit):
    """ Adapts a beaker session object to the interface expected of Zope sessions.
    """

    security = ClassSecurityInfo()
    security.setDefaultAccess('allow')
    security.declareObjectPublic()

    def __init__(self, session):
        self.data = self.session = session

    #
    # IMapping methods
    #

    clear = session_mutator(UserDict.clear)
    update = session_mutator(UserDict.update)
    setdefault = session_mutator(UserDict.setdefault)
    pop = session_mutator(UserDict.pop)
    popitem = session_mutator(UserDict.popitem)
    __setitem__ = session_mutator(UserDict.__setitem__)
    __delitem__ = session_mutator(UserDict.__delitem__)
    set = __setitem__
    __guarded_setitem__ = __setitem__
    __guarded_delitem__ = __delitem__
    delete = __delitem__

    def __len__(self):
        try:
            return self.data.__len__()
        except AttributeError:
            return len(self.data.keys())

    #
    # ISessionDataObject
    #

    def getId(self):
        return self.session.id

    def invalidate(self):
        self.session.invalidate()

    def isValid(self):
        return True

    def getCreated(self):
        return time.mktime(self.session['_creation_time'].timetuple())

    getContainerKey = getId

    #
    # compatibility with standard persistent Zope sessions
    # 

    def _get_p_changed(self):
        return 1
    def _set_p_changed(self, v):
        if v:
            self.session.save()
    _p_changed = property(_get_p_changed, _set_p_changed)

InitializeClass(BeakerSessionDataObject)
