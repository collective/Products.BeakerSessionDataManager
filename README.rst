Introduction
============

``Products.BeakerSessionDataManager`` is a replacement for the default Zope 2
session implementation.  It uses `Beaker`_ as a backend (via `collective.beaker`_)
and adapts the Beaker session to provide the same interface as a normal Zope
session.

Beaker is a better alternative to the default session implementation for several
reasons:

 * The Zope session implementation does not perform well in high-write scenarios.
 * Beaker provides better flexibility in where session data is actually stored.
 * Beaker is used and maintained outside of the Zope ecosystem.

.. Note::
   If you are developing a product that needs sessions but are not already
   using Zope sessions, you should probably just use collective.beaker
   directly. This product is meant for use with existing add-ons that already
   use Zope sessions (i.e. request.SESSION).

.. _`Beaker`: http://beaker.groovie.org/
.. _`collective.beaker`: http://pypi.python.org/pypi/collective.beaker

Installation
------------

1. Add the Products.BeakerSessionDataManager egg to your buildout::

    [instance]
    eggs =
        Products.BeakerSessionDataManager

2. Make sure that buildout adds Beaker configuration to zope.conf. For example::

    zope-conf-additional =
        <product-config beaker>
            session.type            file
            session.data_dir        ${buildout:directory}/var/sessions/data
            session.lock_dir        ${buildout:directory}/var/sessions/lock
            session.key             beaker.session
            session.secret          secret
        </product-config>

   The "secret" should be replaced with a unique string for your system. It
   must be the same for all Zope instances using the same session store.

   See the `collective.beaker`_ docs for more details on configuration.

3. In the ZMI, delete the ``session_data_manager`` object and add a
   ``Beaker Session Data Manager``.

Notes
-----

* Beaker does not automatically clean up old sessions, so you may want to set
  up a cron job to take care of this.
