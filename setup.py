from setuptools import setup

setup(
    name='ratelimitpy',
    version='0.1',
    long_description=__doc__,
    packages=['ratelimitpy'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)
