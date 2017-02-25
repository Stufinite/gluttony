from distutils.core import setup

setup(
    name = 'gluttonyTw',
    packages = ['gluttonyTw', 'gluttonyTw/view'],
    version = '1.8',
    description = 'An API for time2eat.',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/Stufinite/gluttonyTw',
    download_url = 'https://github.com/Stufinite/gluttony/archive/v1.8.tar.gz',
    keywords = ['time2eat', 'campass'],
    classifiers = [],
    license='GPL.0',
    install_requires=[
        'djangoApiDec==1.2',
    ],
    zip_safe=True,
)
