from setuptools import setup

setup(
    name='xs1_api_client',
    version='1.0',
    description='A library to get and set values of the EZcontrol XS1 Gateway',
    license='GPLv3+',
    author='Markus Ressel',
    author_email='mail@markusressel.de',
    url='https://www.markusressel.de',
    packages=['xs1_api_client']
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'requests',
        'json',
        'logging'
    ]
)
