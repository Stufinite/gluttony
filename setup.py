from distutils.core import setup

setup(
    name = 'gluttony_tw',
    packages = ['gluttony_tw'],
    version = '1.0',
    description = 'A API which will return Course of specific Dept. and also Course which you can enroll at that time.',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/Stufinite/gluttony_tw',
    download_url = 'https://github.com/Stufinite/gluttony_tw/archive/v1.0.tar.gz',
    keywords = ['time2eat', 'campass'],
    classifiers = [],
    license='GNU3.0',
    install_requires=[
        'djangoApiDec==1.2',
    ],
    zip_safe=True
)
