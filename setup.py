import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as readme:
    README = readme.read().split('h1>\n\n', 2)[1]

setup(
    name='django-postgres-extra',
    version='1.21a12',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Bringing all of PostgreSQL\'s awesomeness to Django.',
    long_description=README,
    url='https://github.com/zak10/django-postgres-extra',
    author='Sector Labs',
    author_email='open-source@sectorlabs.ro',
    keywords=['django', 'postgres', 'extra', 'hstore', 'ltree'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
