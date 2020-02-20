from setuptools import setup
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent / 'tests'))

setup(
    name='pegtree',
    version='0.9.2',
    url='https://github.com/KuramitsuLab/pegtree.git',
    license='MIT',
    author='Kimio Kuramitsu',
    description='PEGTree for Python and JavaScript',
    install_requires=['setuptools'],
        packages=['pegtree'],
        package_data={'pegtree': ['grammar/*.tpeg',
                                  'grammar/*/*.txt']},
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
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ],
    test_suite='test_all.suite'
)
