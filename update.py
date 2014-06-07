#!python

from __future__ import print_function

import json
import sys
import urllib2

outPath = "modules.json"

if __name__ == "__main__" :
	try:
		result = urllib2.urlopen("https://api.github.com/users/dofmod/repos")
	except urllib2.HTTPError:
		print("Repositories request error", file=sys.stderr)
		exit()

	repositories = json.loads(result.read())
	modsInfos = []
	for repository in repositories:
		if repository["name"] == "MarketPlace" or repository["name"] == "DofModUtils":
			continue

		try:
			result = urllib2.urlopen("https://raw.githubusercontent.com/dofmod/{}/master/mod.json".format(repository["name"]))
		except urllib2.HTTPError as error:
			if error.code == 404:
				print("No mod.json file in the repository {}".format(repository["name"]), file=sys.stderr);
				continue

			print("Repository {} request error".format(repository["name"]), file=sys.stderr)
			continue

		modsInfos.append(json.loads(result.read())[0])

	if len(modsInfos):
		with open(outPath, "w") as outFile:
			outFile.write(json.dumps(modsInfos))


