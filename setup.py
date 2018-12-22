from setuptools import setup
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent / 'tests'))

setup(
	name = 'pegpy',
    version = '0.1.0',
    url = 'https://github.com/KuramitsuLab/pegpy.git',
    license = 'KuramitsuLab',
    author = 'KuramitsuLab',
    description = 'Nez Parser for Python',
    install_requires = ['setuptools'],
	packages = ['pegpy', 'pegpy.gparser', 'pegpy.origami', 'pegpy.playground'],
	package_data = {'pegpy': ['grammar/*.tpeg', 'grammar/*.gpeg', 'origami/*.origami'],
					'pegpy.playground': [
						'cgi-bin/compile.cgi',
						'css/*.css', 'css/*.map',
						'fonts/*.*',
						'jade/*.jade',
						'js/*.js', 'js/ace/*.js', 'js/ace/snippets/*.js',
						'typings/jquery/jquery.d.ts',
						'gulpfile.js', 'index.html', 'index.js', 'index.ts', 'package.json',
						]},
	entry_points = {
		'console_scripts': [
			'pegpy = pegpy.main:main'
		]
	},
	test_suite = 'test_all.suite'
)
