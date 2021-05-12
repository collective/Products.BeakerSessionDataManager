# -*- coding: utf-8 -*-


def initialize(context):

    from Products.BeakerSessionDataManager.sessiondata import (
        addBeakerSessionDataManager,
    )
    from Products.BeakerSessionDataManager.sessiondata import (
        addBeakerSessionDataManagerForm,
    )
    from Products.BeakerSessionDataManager.sessiondata import BeakerSessionDataManager

    context.registerClass(
        BeakerSessionDataManager,
        constructors=(addBeakerSessionDataManagerForm, addBeakerSessionDataManager),
        icon="www/sdm.gif",
    )
