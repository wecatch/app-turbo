from setuptools import setup, find_packages
import sys


version = __import__('turbo').version


install_requires = [

]

for k in ['pymongo', 'requests', 'redis', 'docopt']:
    try:
        __import__(k)
    except ImportError:
        install_requires.append(k)

kwargs = {}
with open('README.md') as f:
    kwargs['long_description'] = f.read()

if sys.version_info < (2, 7):
    install_requires.append('unittest2')
    install_requires.append('tornado<=4.3.0')
else:
    install_requires.append('tornado')

setup(
    name="turbo",
    version=version,
    author="Wecatch.me",
    author_email="wecatch.me@gmail.com",
    url="http://github.com/wecatch/app-turbo",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="turbo is a engine for fast web development based in tornado, mongodb, redis",
    packages=find_packages(),
    install_requires=install_requires,
    scripts=['turbo/bin/turbo-admin'],
    **kwargs
)
