# -*- coding: utf-8 -*-

from zope.interface.common.mapping import IMapping


class ISessionDataObject(IMapping):
    """Supports a mapping interface plus expiration- and container-related
    methods"""

    def getId():
        """
        Returns a meaningful unique id for the object.  Note that this id
        need not the key under which the object is stored in its container.
        """

    def invalidate():
        """
        Invalidate (expire) the transient object.

        Causes the transient object container's "before destruct" method
        related to this object to be called as a side effect.
        """

    def isValid():
        """
        Return true if transient object is still valid, false if not.
        A transient object is valid if its invalidate method has not been
        called.
        """

    def getCreated():
        """
        Return the time the transient object was created in integer
        seconds-since-the-epoch form.
        """

    def getContainerKey():
        """
        Return the key under which the object was placed in its
        container.
        """

    def set(k, v):
        """Alias for __setitem__"""

    def __guarded_setitem__(k, v):
        """Alias for __setitem__"""

    def delete(k):
        """Alias for __delitem__"""

    def __guarded_delitem__(k):
        """Alias for __delitem__"""
