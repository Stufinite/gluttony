from distutils.core import setup

setup(
    name = 'gluttonyTw',
    packages = ['gluttonyTw', 'gluttonyTw/view'],
    version = '1.4',
    description = 'An API for time2eat.',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/Stufinite/gluttonyTw',
    download_url = 'https://github.com/Stufinite/gluttony/archive/v1.4.tar.gz',
    keywords = ['time2eat', 'campass'],
    classifiers = [],
    license='GNU3.0',
    install_requires=[
        'djangoApiDec==1.2',
    ],
    zip_safe=True,
)
