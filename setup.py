from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='vuams-markers',
    url='https://github.com/solo-fsw/vuams-markers',
    author='Evert Dekker, Kerwin Olfers, Jens van Bijsterveld',
    author_email='labsupport@FSW.leidenuniv.nl',
    packages=['vuams-markers'],
    install_requires=['pyserial'],
    version='0.1',
    license='GPLv3',
    description='A python package for sending markers to the vu-ams 5FS.',
    # long_description=open('README.txt').read(),
)