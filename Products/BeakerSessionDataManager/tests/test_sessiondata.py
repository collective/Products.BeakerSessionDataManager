import unittest2 as unittest
from zope.component import provideAdapter
import zope.component.testing


class TestBeakerSessionDataManager(unittest.TestCase):
    
    def setUp(self):
        from collective.beaker.testing import TestSession
        from collective.beaker.interfaces import ISession
        from zope.publisher.interfaces import IRequest
        def testingSession(request):
            return request.environ.setdefault('collective.beaker.testing.session', TestSession())
        provideAdapter(testingSession, [IRequest], ISession)
    
    def tearDown(self):
        zope.component.testing.tearDown()
    
    def _getTargetClass(self):
        from Products.BeakerSessionDataManager.sessiondata import BeakerSessionDataManager
        return BeakerSessionDataManager
    
    def _makeOne(self, *args, **kw):
        sdm = self._getTargetClass()(*args, **kw)
        from Testing.makerequest import makerequest
        return makerequest(sdm)
    
    def test_interface(self):
        from zope.interface.verify import verifyClass
        from Products.Sessions.interfaces import ISessionDataManager
        verifyClass(ISessionDataManager, self._getTargetClass())

    def test___init__(self):
        sdm = self._makeOne(title = 'Beaker')
        self.assertEqual('Beaker', sdm.title)

    def test_getSessionData(self):
        sdm = self._makeOne()
        data = sdm.getSessionData()
        from Products.BeakerSessionDataManager.interfaces import ISessionDataObject
        self.assertTrue(ISessionDataObject.providedBy(data))
        from collective.beaker.interfaces import ISession
        self.assertTrue(ISession.providedBy(data.session))

    def test_hasSessionData(self):
        sdm = self._makeOne()
        self.assertTrue(sdm.hasSessionData())
    
    def test_getSessionDataByKey(self):
        # not implemented
        sdm = self._makeOne()
        from Products.Sessions.SessionDataManager import SessionDataManagerErr
        self.assertRaises(SessionDataManagerErr, sdm.getSessionDataByKey, 'foo')

    def test_getBrowserIdManager(self):
        # not implemented
        sdm = self._makeOne()
        from Products.Sessions.SessionDataManager import SessionDataManagerErr
        self.assertRaises(SessionDataManagerErr, sdm.getBrowserIdManager)


class TestBeakerSessionDataObject(unittest.TestCase):
    
    def _getTargetClass(self):
        from Products.BeakerSessionDataManager.sessiondata import BeakerSessionDataObject
        return BeakerSessionDataObject
    
    def test_interface(self):
        from zope.interface.verify import verifyClass
        from Products.BeakerSessionDataManager.interfaces import ISessionDataObject
        verifyClass(ISessionDataObject, self._getTargetClass())
