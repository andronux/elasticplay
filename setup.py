from setuptools import setup


setup(
	name='mp3',
	version='1.0',
	py_modules=['mp3'],
	install_requires=[
		'Click',
	],
	entry_points='''
		[console_scripts]
		mp3=mp3:cli
	''',
)
