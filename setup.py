from setuptools import setup

setup(
	name = 'pegpy',
    version = '0.1.0',
    url = 'https://github.com/KuramitsuLab/pegpy.git',
    license = 'KuramitsuLab',
    author = 'KuramitsuLab',
    description = 'Nez Parser for Python',
    install_requires = ['setuptools'],
	packages = ['pegpy', 'pegpy.gpeg'],
	package_data = {'pegpy': ['../grammar/*.tpeg']},
	entry_points = {
		'console_scripts': [
			'pegpy = pegpy.main:main',
		]
	}
)
