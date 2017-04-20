from setuptools import setup, find_packages

setup(
    name='statjson',
    #version - in setup.cfg
    packages=find_packages(),
    license='MIT',
    author='John Thorvald Wodder II',
    author_email='statjson@varonathe.org',
    ###keywords='',
    description='stat(2) output as JSON',
    #long_description - in setup.cfg
    ###url='https://github.com/jwodder/statjson',

    python_requires='~=3.3',
    install_requires=[],

    classifiers=[
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
       #'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: POSIX',

        'License :: OSI Approved :: MIT License',

        ###
    ],

    entry_points={
        "console_scripts": [
            "statjson = statjson.__main__:main",
        ]
    },
)
