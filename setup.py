from setuptools import setup
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent / 'tests'))

'''
python3 -m unittest
vim setup.py
rm -rf dist/
python3 setup.py sdist bdist_wheel
twine upload --repository pypi dist/*
'''

setup(
    name='pegtree',
    version='0.9.16',
    url='https://github.com/KuramitsuLab/pegtree.git',
    license='MIT',
    author='Kimio Kuramitsu',
    description='PEGTree for Python',
    #install_requires=['setuptools'],
        packages=['pegtree'],
        package_data={'pegtree': ['grammar/*.tpeg', 'grammar/*.pegtree',
                                  'grammar/*/*.txt',
                                  'code/*.txt', 'cjdic/*.txt']},
    entry_points={
        'console_scripts': [
            'pegtree = pegtree.main:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ],
    test_suite='test_all.suite'
)
