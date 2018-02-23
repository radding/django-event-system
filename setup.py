import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-event-system',
    version='0.1.0.dev3',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',  # example license
    description='A simple package that implements an event system in django',
    long_description=README,
    url='http://yoseph.tech/',
    author='Yoseph Radding',
    author_email='yoseph@shuttl.io',
    install_requires=[
        'gevent',
        'greenlet',
        'pytz',
    ],
    python_requires='>=3.4',
    keywords="django events events for django",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    project_urls={
        'Documentation': 'https://github.com/radding/django-events/blob/master/README.md',
        'Source': 'https://github.com/radding/django-events/',
        'Tracker': 'https://github.com/radding/django-events/issues',
    },
)