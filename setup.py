from setuptools import setup, find_packages

setup(
    name='xs1_api_client',
    version='2.0.0',
    description='A library to get and set values of the EZcontrol XS1 Gateway',
    license='GPLv3+',
    author='Markus Ressel',
    author_email='mail@markusressel.de',
    url='https://www.markusressel.de',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'requests', 'urllib3',
        # 'logging'
    ]
)
