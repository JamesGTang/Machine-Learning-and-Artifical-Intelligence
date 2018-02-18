# this is a python program to solve the q3
# comp424 A1 the original question is:
# Consider the following function: Y= sin(X2/2)/log2(X+4), in the range X=[0, 10].# 
# Apply hill-climbing, starting from each of the following starting points: 
#X0={0, 1, 2, …, 10} and step sizes Δ𝑋 = {0.01, 0.02, …, 0.1}

import math
# x is the starting point
# using list as data structure 
xList = {0,1,2,3,4,5,6,7,8,9,10}
incrementList = {0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10}

# hill climb algorithm
def hillclimb(x,increment):
	#when first called, calculate which direction to go
	y=0
	val=list()
	counter=0
	if(calc(x+increment)>calc(x)):
		#keep going until the hill
		while(calc(x+increment)>calc(x)):
			x+=increment
			y=calc(x)
			counter+=1	
		val.append(x)
		val.append(y)
		val.append(counter)	
	elif(calc(x-increment)>calc(x)):
		while(calc(x-increment)>calc(x)):
			x-=increment
			y=calc(x)
			counter+=1
		val.append(x)
		val.append(y)
		val.append(counter)	
	else:
		x+=increment
		y=calc(x+increment)
		val.append(x)
		val.append(y)
		val.append(counter)	
	#we found a hill at this point	
	return val
#calculate using x value
def calc(x):
	# default as radian
	if (x == 0):
		return 0
	else:
		return math.sin(x*x)/math.log((x+4),2)*2.339

def main():
	print("Report for hillclimb algorithm")
	print("______________________________")
	print("    X     Increment   Steps Xfinal   YFinal")
	orderedList=sorted(incrementList)

	for x in xList:
		for increment in orderedList: 
			result=hillclimb(x,increment) 
			print("{:6g}   {:6g}   {:6g}   {:6g}   {:6g}".format(x,increment,result[2],result[0],result[1]))

if __name__ == "__main__": main()

