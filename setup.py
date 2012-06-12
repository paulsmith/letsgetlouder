from setuptools import setup, find_packages

setup(
    name='letsgetlouder.com',
    version='0.1',
    description='Django community pledge site',
    url='http://letsgetlouder.com/',
    install_requires=['Django==1.4', 'django-social-auth==0.6.9'],
    packages=find_packages(),
    license='BSD'
)
