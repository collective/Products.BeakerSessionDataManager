def initialize(context):

    from Products.BeakerSessionDataManager.sessiondata import BeakerSessionDataManager
    from Products.BeakerSessionDataManager.sessiondata import (
        addBeakerSessionDataManager,
    )
    from Products.BeakerSessionDataManager.sessiondata import (
        addBeakerSessionDataManagerForm,
    )

    context.registerClass(
        BeakerSessionDataManager,
        constructors=(addBeakerSessionDataManagerForm, addBeakerSessionDataManager),
        icon="www/sdm.gif",
    )
