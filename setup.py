from setuptools import setup
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent / 'tests'))

setup(
    name='pegpy',
    version='0.9.6',
    url='https://github.com/KuramitsuLab/pegpy.git',
    license='KuramitsuLab',
    author='Kimio Kuramitsu and His Laboratory',
    description='Tree PEG for Python',
    install_requires=['setuptools'],
        packages=['pegpy'],
        package_data={'pegpy': ['grammar/*.tpeg',
                                'grammar/*.peg', 'parser/*.*']},
    entry_points={
        'console_scripts': [
            'pegpy = pegpy.main:main'
        ]
    },
    test_suite='test_all.suite'
)
