import os;

STAY = "STAY";
INNER = "INNER";
NEXT = "NEXT";
DONE = "DONE";
DONE_AND_CONSUME = "DONE_AND_CONSUME";

def processSection(state, text):
	#print "Section: " + text;
	if (text == '_______________________________________________________________________________\n'):
		return (DONE, [], state)
	return (STAY, [], state);

def processMonsterListing(state, text):
	print "Walkthrough Monsters: " + text
	if (text == '_________________________________________________\n'):
		return (DONE_AND_CONSUME, [], state)

	return (STAY, [], state)

def processWalkthroughSectionTitle(state, text):
	print "Walkthrough SectionTitle: " + text;
	if (text == '_________________________________________________\n'):
		return (DONE_AND_CONSUME, processWalkthroughSection, state)
	stripped = text.strip();
	if (stripped.startswith('[')):
		state['walkthrough_subsection'] = stripped
		print stripped
	elif (stripped == 'Pokemon           Type       Version  Rate  Level'):
		return (NEXT, processMonsterListing, state);
		
	return (STAY, [], state);

def processTypeShorthand(state, text):
	#print "Type Shorthand: " + text;
	if (text == '_________________________________________________\n'):
		return (DONE, [], state);

	t = text.split();
	state['types'][t[0]] = t[1];
	return (STAY, [], state);

def processWalkthroughSection(state, text):
	print "Walkthrough: " + text;
	if (text == '_________________________________________________\n'):
		return (INNER, processWalkthroughSectionTitle, state)
	if (text == '--------------\n' and state['previous'] == 'Type Shorthand\n'):
		return (INNER, processTypeShorthand, state)
	return (STAY, [], state);

def processSectionTitle(state, text):
	#print "Title: " + text;
	if (text == '_______________________________________________________________________________\n'):
		if (state['title'] == "Table of Contents"):
			return (NEXT, processSection, state)
		elif (state['title'] == "I. The Walkthrough"):
			return (NEXT, processWalkthroughSection, state)
	elif (len(text.strip()) > 0):
		state['title'] = text.strip();
	return (STAY, [], state);

def baseProcessor(state, text):
	#print "Base: " + text;
	if (text == '_______________________________________________________________________________\n'):
		return (INNER, processSectionTitle, state)
	return (STAY, [], state);

def processZerokidFaq():
	fileName = "/home/local/ANT/rafkindd/Downloads/Pokemen_Red_Faq_by_zerokid.txt";

	processorStack = [];
	processorStack.append(baseProcessor);

	transition = "";
	newProc = [];
	state = {};
	state['types'] = {};
	state['areas'] = {};

	with open(fileName, "r") as inFile:
		for line in inFile:
			iterations = 1;
			while (iterations > 0):
				currentProcessor = processorStack[len(processorStack)-1]
				(transition, newProc, state) = currentProcessor(state, line);
				iterations -= 1;
				if (transition == INNER):
					processorStack.append(newProc);
				elif (transition == NEXT):
					processorStack[len(processorStack)-1] = newProc;
				elif (transition == DONE):
					currentProcessor = processorStack.pop();
					iterations += 1;
				elif (transition == DONE_AND_CONSUME):
					currentProcessor = processorStack.pop();
			state['previous'] = line

if __name__ == "__main__":
	processZerokidFaq();
