# this is a python program to solve the q3(b)
# comp424 A1 the original question is:
# Repeat using simulated annealing with a range of different temperatures 
# and annealing schedules (of your choosing). Consider each of the different 
# starting points in (a). Consider only those step sizes from part (a) that produced a 
# good result (use your own judgment in defining this; briefly explain your reasoning 
# and method.)
import math
import random

temperature={125,250,500,750,1000,1250,1500}
cooling={1,2,3,4,5,6,7}
xStart={1,4,7}

# hill climb algorithm
def simulated_annealing(temp,cool,x):
	#when first called, calculate which direction to go
	val=list()
	counter=0
	xNew=0
	while(temp>1):
		# generate a random new x between 0 and 10
		xNew=random.random()*10
		if(randomWalk(x,xNew,temp)==1):
			#switch to new node
			x=xNew
		else:
			x=x
		counter+=1
		temp=temp-cool
	val.append(x)
	val.append(calc(x))
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

#decide given the current temperature, whether jump to other node or not
def randomWalk(xOld,xNew,temp):
	# if new node is bigger than old node, always jump
	if(calc(xOld)<=calc(xNew)):
		return 1	
	elif (random.random()*temp>=50):
		#generate a random number between 0 and 1, if the number* temperature is more than 50
		return 1
	else:
		# the temperature is cooled
		return 0		

def main():
	print("Report for simulated annealing algorithm")
	print("________________________________________")

	print("Temperature used: ",temperature)
	print("Cooling used: ",cooling)

	print("RandX    Temp     Cooling   Steps  Xfinal   YFinal")
	print("__________________________________________________")
	
	for x in sorted(xStart):
		for cool in cooling: 
			for temp in temperature:
					result=simulated_annealing(temp,cool,x) 
					print("{:6g}   {:6g}   {:6g}   {:6g}   {:6g}   {:6g}".format(x,temp,cool,result[2],result[0],result[1]))

if __name__ == "__main__": main()
