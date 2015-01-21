from setuptools import setup, find_packages


version = '.'.join((__import__('turbo').version)[:-1])

setup(
    name="turbo",
    version=version,
    packages = ["turbo", "turbo.cache", "turbo.template"],
    author="Wecatch.me",
    author_email="wecatch.me@gmail.com",
    url="http://github.com/wecatch/app-turbo",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="Turbo is a engine for fast web development based in tornado, mongodb, redis",
    packages=find_packages(),
    install_requires=[
        'tornado',
        'pymongo',
        'requests',
        'redis',
    ],
)