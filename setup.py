from setuptools import setup, find_packages


version = __import__('turbo').version


install_requires = [

]

for k in ['tornado','pymongo', 'requests', 'redis', 'docopt']:
    try:
        __import__(k)
    except ImportError:
        install_requires.append(k)

setup(
    name="turbo",
    version=version,
    author="Wecatch.me",
    author_email="wecatch.me@gmail.com",
    url="http://github.com/wecatch/app-turbo",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="turbo is a engine for fast web development based in tornado, mongodb, redis",
    packages=find_packages(exclude=('turbo.template')),
    install_requires=install_requires,
    scripts=['turbo/bin/turbo-admin'],
)
