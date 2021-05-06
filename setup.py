from setuptools import setup, find_packages
import io

def read_all(f):
    with io.open(f, encoding="utf-8") as I:
        return I.read()


requirements = list(map(str.strip, open("requirements.txt").readlines()))


setup(
    name='redisgraph',
    version='2.3.0',
    description='RedisGraph Python Client',
    long_description=read_all("README.md"),
    long_description_content_type='text/markdown',
    url='https://github.com/RedisGraph/redisgraph-py',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Topic :: Database',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 5 - Production/Stable'
    ],
    author='RedisLabs',
    keywords='Redis Graph',
    author_email='oss@redislabs.com'
)
