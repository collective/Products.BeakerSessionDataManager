import unittest2 as unittest


class TestBeakerSessionDataManager(unittest.TestCase):
    
    def _getTargetClass(self):
        from Products.BeakerSessionDataManager.sessiondata import BeakerSessionDataManager
        return BeakerSessionDataManager
    
    def test_interface(self):
        from zope.interface.verify import verifyClass
        from Products.Sessions.interfaces import ISessionDataManager
        verifyClass(ISessionDataManager, self._getTargetClass())


class TestBeakerSessionDataObject(unittest.TestCase):
    
    def _getTargetClass(self):
        from Products.BeakerSessionDataManager.sessiondata import BeakerSessionDataObject
        return BeakerSessionDataObject
    
    def test_interface(self):
        from zope.interface.verify import verifyClass
        from Products.BeakerSessionDataManager.interfaces import ISessionDataObject
        verifyClass(ISessionDataObject, self._getTargetClass())
