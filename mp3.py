#!/usr/bin/python
import click
import json
import pycurl
import urllib
import wget
import colorama

from StringIO import StringIO

API_BASE = 'http://databrainz.com/api/'
SEARCH = 'search_api.cgi'
DATA = 'data_api_new.cgi'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@click.group()
def cli():
	pass


@cli.command()
@click.option('--count', default=10, show_default=True, help='number of result to show')
@click.argument('name', required=True)
def search(name,count):
	""" Search MP3  """
	params = {'qry': name, 'format': 'json', 'mh': count}
	buffer = StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, API_BASE + SEARCH + '?' + urllib.urlencode(params))
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	c.close()
	body = buffer.getvalue()
	#print(bcolors.OKBLUE + body)
	res = json.loads(body)
	print(str(len(res['results'])) + ' results found')
	for entry in res['results']:
		print(bcolors.OKGREEN + entry['artist'] + ' - ' + bcolors.OKBLUE + entry['title'] + ' > uri: '+ bcolors.WARNING + entry['url'])
	if click.confirm('Anything interesting to download?'):
		tag = click.prompt('Sweet! Which one you\'d like? ', type=str)
		download(tag)
	else:
		exit()
	#print(json.dumps(res['results'],sort_keys=True,indent=2,separators=(',', ': ')))
	#print(res['results'][0]['description'])
	#print(res['results'])
	#curl 'http://databrainz.com/api/search_api.cgi?qry=daft&format=json&mh=50'

	#curl -I 'http://databrainz.com/api/data_api_new.cgi?id=f969f1c55baacf172ad4b0aa295c1402&r=api&format=json'

#@cli.command()
#@click.argument('tag', required=True)
def download(tag):
	""" this will just show the ID of the desired mp3 """
	print('you entered '+ tag)
	params = {'id': tag, 'format': 'json', 'r': 'api'}
	buffer = StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, API_BASE + DATA + '?' + urllib.urlencode(params))
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	c.close()
	body = buffer.getvalue()
	#print(body)
	res = json.loads(body)
	#print(json.dumps(res['song'],sort_keys=True,indent=2,separators=(',', ': ')))
	getIt(res['song']['url'])

#@cli.command()
#@click.confirmation_option(help='Are you sure you want to download this music?')
def getIt(tag):
	click.secho('Downloading the music!')
	fn = wget.download(tag)
	click.secho('Congrats! You just downloaded '+fn , fg='green')	

#if __name__ == '__main__':
#	search()
#	getFile()
