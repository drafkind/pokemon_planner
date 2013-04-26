from bs4 import BeautifulSoup

docstr = ""

with open("42712.htm", "r") as myfile:
	docstr = myfile.read()

soup = BeautifulSoup(docstr);

print(soup.prettify());
