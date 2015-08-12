from setuptools import setup


setup(
	name='elasticplay',
	version='1.0',
	py_modules=['mp3'],
	install_requires=[
		'Click',
		'colorama',
	],
	entry_points='''
		[console_scripts]
		elasticplay=mp3:cli
	''',
)
