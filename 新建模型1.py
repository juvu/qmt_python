def init(ContextInfo):
	print(ContextInfo.capital)

def handlebar(ContextInfo):
	index = ContextInfo.barpos
	realtimetag = ContextInfo.get_bar_timetag(index)
	print(realtimetag)