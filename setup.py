from setuptools import setup, find_packages
setup(
    name='redisgraph',
    version='1.1',

    description='RedisGraph Python Client',
    url='https://github.com/swilly22/redisgraph-py',
    packages=find_packages(),
    install_requires=['redis', 'PTable'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database'
    ]
)