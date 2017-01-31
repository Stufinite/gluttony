from distutils.core import setup

setup(
    name = 'gluttony_tw',
    packages = ['gluttony_tw', 'gluttony_tw/view'],
    version = '1.2',
    description = 'An API for time2eat.',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/Stufinite/gluttony_tw',
    download_url = 'https://github.com/Stufinite/gluttony/archive/v1.2.tar.gz',
    keywords = ['time2eat', 'campass'],
    classifiers = [],
    license='GNU3.0',
    install_requires=[
        'djangoApiDec==1.2',
    ],
    zip_safe=True,
)
