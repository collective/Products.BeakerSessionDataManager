from setuptools import setup, find_packages

version = "2.2.dev0"

requires = [
    "setuptools",
    "collective.beaker",
    "Zope2",
    "zope.interface",
    "unittest2",
    "Products.Sessions",
]

setup(
    name="Products.BeakerSessionDataManager",
    version=version,
    description="Zope2 session implementation using Beaker",
    long_description=open("README.rst").read() + "\n" + open("CHANGES.rst").read(),
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Zope :: 4",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="zope sessions beaker",
    author="David Glick, Groundwire",
    author_email="davidglick@groundwire.org",
    url="http://github.com/davisagli/Products.BeakerSessionDataManager",
    license="MIT",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["Products"],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={},
)
