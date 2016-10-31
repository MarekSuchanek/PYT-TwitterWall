from setuptools import setup, find_packages

with open('README') as f:
    long_description = ''.join(f.readlines())

setup(
    name='twitterwall',
    version='0.3',
    keywords='twitter feed cli web tweet wall',
    description='Simple CLI & WEB based Twitter tweets feed',
    long_description=long_description,
    author='Marek Suchánek',
    author_email='suchama4@fit.cvut.cz',
    license='MIT',
    url='https://github.com/MarekSuchanek/PYT-TwitterWall',
    zip_safe=False,  # http://flask.pocoo.org/docs/0.11/patterns/distribute/
    packages=find_packages(),
    package_data={
        'twitterwall': [
            'static/*.*',
            'static/fonts/*.*',
            'static/images/*.*',
            'templates/*.html'
        ]
    },
    entry_points={
        'console_scripts': [
            'twitterwall = twitterwall.cli:main',
        ],
    },
    install_requires=[
        'Flask>=0.10.0',
        'Flask-Injector>=0.8.0',
        'injector>=0.9.0',
        'Jinja2>=2.6',
        'click>=6.6',
        'requests>=2.10.0'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-pep8'
        'pytest-cov',
        'pytest-sugar',
        'betamax',
        'flexmock',
    ],
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications',
        'Topic :: Internet',
        'Topic :: Sociology'
    ],
)
