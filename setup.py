from distutils.core import setup

setup(
    name = 'gluttonyTw',
    packages = ['gluttonyTw', 'gluttonyTw/view'],
    version = '2.1',
    description = 'An API for time2eat.',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/Stufinite/gluttonyTw',
    download_url = 'https://github.com/Stufinite/gluttony/archive/v2.1.tar.gz',
    keywords = ['time2eat', 'campass'],
    classifiers = [],
    license='GPL3.0',
    install_requires=[
        'djangoApiDec',
    ],
    zip_safe=True,
)
