import urllib;
import os;
import errno;
import bs4;
import StringIO;

CACHE_DIR = "cache";
try:
	os.makedirs(CACHE_DIR);
except OSError as exc:
	if exc.errno == errno.EEXIST and os.path.isdir(CACHE_DIR):
		pass
	else: raise

def getSoupFor(url, local):
	localFileName = CACHE_DIR + "/" + local;
	(filename, headers) = urllib.urlretrieve(url, localFileName);
	return bs4.BeautifulSoup(open(filename, "r"));

def processLandoKashmirFaq():
	soup = getSoupFor("http://www.gamefaqs.com/gameboy/367023-pokemon-red-version/faqs/42712", "42712.html");

	documentText = soup.find('div', id='body').pre.text;
	buffer = StringIO.StringIO(documentText);

	sectionTransitions = {}
	sectionTransitions["TOC"] = "A";
	sectionTransitions["A"] = "B";
	sectionTransitions["B"] = "C";
	sectionTransitions["C"] = "D";
	sectionTransitions["D"] = "E";

	currentSection = "TOC";
	for currentLine in buffer:
		if (currentLine.startswith("####")):
			currentSection = sectionTransitions[currentSection];
		print currentSection;

if __name__ == "__main__":
	processLandoKashmirFaq();
