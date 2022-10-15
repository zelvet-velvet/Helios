ewe=[]
owo=[[3,2],[4,5],[2,9]]

for l in range(len(owo)):
	l = True
	try:
		if abs(ewe[l][0]-owo[l][0])<15) and abs(ewe[l][1]-owo[l][1])<15):
			ewe[l][2]=True
		else:
		 	ewe[l][0] = owo[l][0]
		 	ewe[l][1] = owo[l][1]
			ewe[l][2] = False
	except:
		if len(owo)<len(ewe):	  

print(ewe[0],ewe[1])
