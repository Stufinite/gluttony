from distutils.core import setup

setup(
    name = 'gluttonyTw',
    packages = ['gluttonyTw', 'gluttonyTw/view'],
    version = '1.2',
    description = 'An API for time2eat.',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/Stufinite/gluttonyTw',
    download_url = 'https://github.com/Stufinite/gluttony/archive/v1.2.tar.gz',
    keywords = ['time2eat', 'campass'],
    classifiers = [],
    license='GNU3.0',
    install_requires=[
        'djangoApiDec==1.2',
        '-e git://github.com/Stufinite/userper.git@20e8161313fb7b247f55ee6c9e4b3764740b1f98#egg=userper'
    ],
    zip_safe=True,
)
