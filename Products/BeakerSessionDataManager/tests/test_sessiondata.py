# -*- coding: utf-8 -*-

from datetime import datetime
from zope.component import provideAdapter

import unittest2 as unittest
import zope.component.testing


class TestBeakerSessionDataManager(unittest.TestCase):
    def setUp(self):
        from collective.beaker.interfaces import ISession
        from collective.beaker.testing import TestSession
        from zope.publisher.interfaces import IRequest

        def testingSession(request):
            return request.environ.setdefault(
                "collective.beaker.testing.session", TestSession()
            )

        provideAdapter(testingSession, [IRequest], ISession)

    def tearDown(self):
        zope.component.testing.tearDown()

    def _getTargetClass(self):
        from Products.BeakerSessionDataManager.sessiondata import (
            BeakerSessionDataManager,
        )

        return BeakerSessionDataManager

    def _makeOne(self, *args, **kw):
        sdm = self._getTargetClass()(*args, **kw)
        from Testing.makerequest import makerequest

        return makerequest(sdm)

    def test_interface(self):
        from Products.Sessions.interfaces import ISessionDataManager
        from zope.interface.verify import verifyClass

        verifyClass(ISessionDataManager, self._getTargetClass())

    def test___init__(self):
        sdm = self._makeOne(title="Beaker")
        self.assertEqual("Beaker", sdm.title)

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

        self.assertRaises(SessionDataManagerErr, sdm.getSessionDataByKey, "foo")

    def test_getBrowserIdManager(self):
        # not implemented
        sdm = self._makeOne()
        from Products.Sessions.SessionDataManager import SessionDataManagerErr

        self.assertRaises(SessionDataManagerErr, sdm.getBrowserIdManager)

    def test_factory(self):
        from Products.BeakerSessionDataManager.sessiondata import (
            addBeakerSessionDataManager,
        )
        from Products.BeakerSessionDataManager.sessiondata import (
            BeakerSessionDataManager,
        )

        class DummyDispatcher(object):
            def _setObject(self, id, ob):
                setattr(self, id, ob)

        dispatcher = DummyDispatcher()
        addBeakerSessionDataManager(dispatcher, "sdm")
        self.assertTrue(isinstance(dispatcher.sdm, BeakerSessionDataManager))

    def test_manage_afterAdd(self):
        sdm = self._makeOne()
        sdm.manage_afterAdd(None, None)
        self.assertTrue(sdm._hasTraversalHook)

    def test_manage_beforeDelete(self):
        sdm = self._makeOne()
        sdm.manage_afterAdd(None, None)
        sdm.manage_beforeDelete(None, None)
        self.assertFalse(hasattr(sdm, "_hasTraversalHook"))


class TestBeakerSessionDataObject(unittest.TestCase):
    def _getTargetClass(self):
        from Products.BeakerSessionDataManager.sessiondata import (
            BeakerSessionDataObject,
        )

        return BeakerSessionDataObject

    def _makeOne(self):
        from collective.beaker.testing import TestSession

        return self._getTargetClass()(TestSession())

    def test_interface(self):
        from Products.BeakerSessionDataManager.interfaces import ISessionDataObject

        self.assertTrue(ISessionDataObject.implementedBy(self._getTargetClass()))

    def test_session_mutator(self):
        from Products.BeakerSessionDataManager.sessiondata import session_mutator
        from collective.beaker.testing import TestSession

        class Dummy(object):
            data = TestSession()

            @session_mutator
            def mutate(self):
                pass

        dummy = Dummy()
        dummy.mutate()
        self.assertTrue(dummy.data._saved)

    def test_getId(self):
        ob = self._makeOne()
        self.assertEqual("test-session", ob.getId())

    def test_invalidate(self):
        ob = self._makeOne()
        ob.invalidate()
        self.assertTrue(ob.session._invalidated)

    def test_isValid(self):
        ob = self._makeOne()
        self.assertTrue(ob.isValid())

    def test_getCreated(self):
        ob = self._makeOne()
        ob.session = {"_creation_time": datetime.now()}
        self.assertTrue(isinstance(ob.getCreated(), float))

    def test_getContainerKey(self):
        ob = self._makeOne()
        self.assertEqual("test-session", ob.getContainerKey())

    def test__p_changed(self):
        ob = self._makeOne()
        ob._p_changed = 1
        self.assertTrue(ob.session._saved)
        self.assertEqual(1, ob._p_changed)

    def test_existence_real_collective_beaker_session(self):
        # Collective.Beaker fakes a session with a Dict which implements
        # __len__. Beaker session uses a lazy interable dict but doesn't
        # implement __len__. A simple truth test fails without __len__.
        from Products.BeakerSessionDataManager.sessiondata import (
            BeakerSessionDataObject,
        )
        from collective.beaker.session import SessionObject

        session = BeakerSessionDataObject(SessionObject({}))
        self.assertTrue(session)
