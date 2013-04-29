import urllib;
import os;
import errno;
import bs4;
import StringIO;
import re;

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

class ParseableSection:
	def __init__(self, name, nextName):
		self.name = name;
		self.nextName = nextName;

	def parse(self, text):
		return;

	def done(self):
		return;

class LandoKashmirWalkthru(ParseableSection):
	def __init__(self, name, nextName):
		ParseableSection.__init__(self, name, nextName)
		self.state = "SECTIONTITLE";
		self.working_subsection_title = "";
		self.oldText = "";

	def parse(self, text):
		previousLineBlank = len(self.oldText.strip(' \t\r\n')) == 0;

		if (text.startswith("____")):
			self.state = "SUBSECTION_DIVIDER";
		elif (self.state == "SUBSECTION_DIVIDER"): 
			self.working_subsection_title = text;
			print text
			self.state = "SUBSECTION_TEXT";
		elif (self.state == "SUBSECTION_TEXT" and previousLineBlank and re.search('\$[0-9]+$', text) != None):
			print text
			self.state = "SUBSECTION_TRAINER";
		elif (self.state == "SUBSECTION_TRAINER"):
			match = re.search('(OR)?\s*([a-zA-Z()]+),\s*level ([0-9]+)\s*-\s*([^(]+)\(([0-9]+) EXP.\)\s*', text); 
			if match:
				print match.groups()
			else:
				self.state = "SUBSECTION_TEXT";
		elif (self.state == "SUBSECTION_TEXT" and previousLineBlank and re.search('Wild Pokemon:\s*$')):
			match = re.search('(\s+) Wild Pokemon:\s*', text);
			print match.groups()
			self.state = "SUBSECTION_WILD"
		elif (self.state == "SUBSECTION_WILD"):
			match = re.search


		#print self.state;
		#print self.name;
	
		self.oldText = text;

	def done(self):
		return;

def processLandoKashmirFaq():
	soup = getSoupFor("http://www.gamefaqs.com/gameboy/367023-pokemon-red-version/faqs/42712", "42712.html");

	documentText = soup.find('div', id='body').pre.text;
	buffer = StringIO.StringIO(documentText);

	sectionTransitions = {}
	sectionTransitions["TOC"] = ParseableSection("TOC", "A");
	sectionTransitions["A"] = ParseableSection("A", "B");
	sectionTransitions["B"] = LandoKashmirWalkthru("B", "C");
	sectionTransitions["C"] = ParseableSection("C", "D");
	sectionTransitions["D"] = ParseableSection("D", "E");
	sectionTransitions["E"] = ParseableSection("E", "");

	currentSection = sectionTransitions["TOC"];
	for currentLine in buffer:
		if (currentLine.startswith("####")):
			currentSection.done();
			currentSection = sectionTransitions[currentSection.nextName];
		currentSection.parse(currentLine);

	currentSection.done();

def processZerokidFaq():
	soup = getSoupFor("http://www.gamefaqs.com/gameboy/367023-pokemon-red-version/faqs/64175", "64175.html");

	documentText = soup.find('div', id='body').pre.text;
	buffer = StringIO.StringIO(documentText);

if __name__ == "__main__":
	processLandoKashmirFaq();
