from setuptools import setup, find_packages
import sys

version = '1.1dev'

requires = [
    'setuptools',
    'collective.beaker',
    'Zope2',
    'zope.interface',
    'unittest2',
    ]

if sys.version_info < (2,6):
    requires.append('ZPublisherEventsBackport')

setup(name='Products.BeakerSessionDataManager',
      version=version,
      description="Zope2 session implementation using Beaker",
      long_description=open("README.rst").read() + "\n" +
                       open("CHANGES.txt").read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Zope2",
        ],
      keywords='zope sessions beaker',
      author='David Glick, Groundwire',
      author_email='davidglick@groundwire.org',
      url='http://github.com/davisagli/Products.BeakerSessionDataManager',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      )
