from setuptools import setup
import sys
sys.path.append('./tests')

setup(
	name = 'pegpy',
    version = '0.1.0',
    url = 'https://github.com/KuramitsuLab/pegpy.git',
    license = 'KuramitsuLab',
    author = 'KuramitsuLab',
    description = 'Nez Parser for Python',
    install_requires = ['setuptools'],
	packages = ['pegpy', 'pegpy.gparser', 'pegpy.origami'],
	package_data = {'pegpy': ['grammar/*.tpeg']},
	entry_points = {
		'console_scripts': [
			'pegpy = pegpy.main:main',
		]
	},
	test_suite='test_all.suite'
)
