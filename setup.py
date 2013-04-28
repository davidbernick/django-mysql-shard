from setuptools import setup, find_packages

setup(
    name = "sqlshards",
    version = "0.1",
    packages=['sqlshards','sqlshards.db','sqlshards.management','sqlshards.db.shards','sqlshards.management.commands'],
    
    # scripts and dependencies
    install_requires = ['setuptools',
                        'Django',
                        ],

    include_package_data = True,
    zip_safe = False,

    # author metadata
    )
