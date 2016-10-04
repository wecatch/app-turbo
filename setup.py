from setuptools import setup, find_packages
import sys
import os


version = __import__('turbo').version


install_requires = [

]

for k in ['pymongo', 'requests', 'redis', 'docopt', 'jinja2']:
    try:
        __import__(k)
    except ImportError:
        install_requires.append(k)

kwargs = {}

readme_path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(readme_path, 'README.rst')) as f:
    kwargs['long_description'] = f.read()

if sys.version_info < (2, 7):
    install_requires.append('unittest2')
    install_requires.append('tornado<=4.3.0')
    install_requires.append('futures')
else:
    install_requires.append('tornado')

setup(
    name="turbo",
    version=version,
    author="Wecatch.me",
    author_email="wecatch.me@gmail.com",
    url="http://github.com/wecatch/app-turbo",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="turbo is a web framework for fast web development based in tornado, mongodb, redis",
    keywords='web framework tornado mongodb',
    packages=find_packages(),
    install_requires=install_requires,
    scripts=['turbo/bin/turbo-admin'],
    **kwargs
)
