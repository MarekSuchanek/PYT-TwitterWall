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
    packages=find_packages(),
    install_requires=[
        'Flask>=0.10.0',
        'Jinja2>=2.6',
        'click>=6.6',
        'requests>=2.10.0'
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
