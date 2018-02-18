# a sample program to perform
# BFS and DFS on a six puzzle
# written by James Tang @ jamesgtang.com

#define goal state
goalState = [0, 1, 2, 5, 4, 3]
startState = [1, 4, 2, 5, 3, 0]

"""
	check if move up opeartion is available
	if available return the operation
	else return null node
"""
def uOperator( searchState ):
	# moves the blank tile up
	new_state = searchState[:]
	# find blank tile index
	index = new_state.index( 0 )

	if index >=2:
		# Swap the values
		temp=new_state[index-3]
		new_state[index-3]=0
		new_state[index]=temp
		#print("New up state")
		return new_state
	else:
		return None
"""
	check if move down opeartion is available
	if available return the operation
	else return null node
"""
def dOperator( searchState ):
	# down the blank tile up
	new_state = searchState[:]
	# find blank tile index
	index = new_state.index( 0 )

	if index <=2:
		# Swap the values
		temp=new_state[index+3]
		new_state[index+3]=0
		new_state[index]=temp
		#print("New d state")
		return new_state
	else:
		return None

"""
	check if move left opeartion is available
	if available return the operation
	else return null node
"""
def lOperator( searchState ):
	# down the blank tile up
	new_state = searchState[:]
	# find blank tile index
	index = new_state.index( 0 )

	if (index != 0) and (index !=3):
		# Swap the values
		temp=new_state[index-1]
		new_state[index-1]=0
		new_state[index]=temp
		#print("New l state")
		return new_state
	else:
		return None

"""
	check if move right opeartion is available
	if available return the operation
	else return null node
"""
def rOperator( searchState ):
	# down the blank tile up
	new_state = searchState[:]
	# find blank tile index

	index = new_state.index( 0 )
	#print(searchState)
	#print("R index: ",index)
	if (index != 2) and (index !=5):
		# Swap the values
		temp=new_state[index+1]
		new_state[index+1]=0
		new_state[index]=temp
		#print("New r state")
		return new_state
	else:
		return None

#check if the operator can be applied to the state
def legalOP(searchNode):	
	legalNode=[]
	# do not go back to previous state
	prevMove=searchNode.operator
	if(uOperator(searchNode.state)!=None and searchNode.operator!="DOWN"):
		legalNode.append(newNode(uOperator(searchNode.state),searchNode,"UP",searchNode.depth+1,0))
	if(dOperator(searchNode.state)!=None and searchNode.operator!="UP"):
		legalNode.append(newNode(dOperator(searchNode.state),searchNode,"DOWN",searchNode.depth+1,0))
	if(lOperator(searchNode.state)!=None and searchNode.operator!="RIGHT"):
		legalNode.append(newNode(lOperator(searchNode.state),searchNode,"LEFT",searchNode.depth+1,0))
	if(rOperator(searchNode.state)!=None and searchNode.operator!="LEFT"):
		legalNode.append(newNode(rOperator(searchNode.state),searchNode,"RIGHT",searchNode.depth+1,0))

	#for node in legalNode:
	#	print("New: ",node.state)	
	return legalNode

# search node data structure
class SearchNode:
	def __init__( self, state, parent, operator, depth, cost ):
		self.state = state
		self.parent = parent
		self.operator = operator		
		self.depth = depth
		self.cost = cost


def newNode(state,parent,operator,depth,cost):
	#return a new search node
	return SearchNode(state,parent,operator,depth,cost)

def isGoalState(state,goalState):
	if(state==goalState):
		return 1
	else:
		return 0		

#check to see if they are any paths unexplored
def isNoPath(BFS):
	if(len(BFS)==0):
		print("No more path!")
		return None

def BFS(startState,goalState):
	# create a new structure
	
	BFS=[]
	# create the initial node
	BFS.append(newNode(startState,None,None,0,0))
	while (True):
		if(len(BFS)==None):			
			return None
		# remove the node at postion 0	
		newSearchNode=BFS.pop(0)
		#print("msg: ",newSearchNode.state,goalState)
		if isGoalState(newSearchNode.state,goalState):
			path=[]
			temp=newSearchNode
			while (True):
				path.insert(0,temp.state)
				if temp.depth ==1:
					break
				temp=temp.parent
			return path	
		BFS.extend(legalOP(newSearchNode))

def DFS(startState,goalState,depth_limit):
	DFS=[]
	explored=[]
	# create the initial node
	DFS.append(newNode(startState,None,None,0,0))
	while (True):
		if(len(DFS)==None):			
			return None
		# remove the node at postion 0	
		newSearchNode=DFS.pop(0)
		explored.append(newSearchNode.state)
		#print("msg: ",newSearchNode.state,goalState)
		if isGoalState(newSearchNode.state,goalState):
			path=[]
			temp=newSearchNode
			while (True):
				path.insert(0,temp.state)
				if temp.depth ==1:
					break
				temp=temp.parent
			return path	
		# always add node to the front of the queue
		if newSearchNode.depth<depth_limit:
			newDFS = legalOP(newSearchNode)
			unexploredDFS=[]
			for state in newDFS:
				if not (state.state in explored):
					unexploredDFS.append(state)
			unexploredDFS.extend(DFS)
			DFS=unexploredDFS
	

def iterative_deepening(startState,goalState,depth):
	for i in range( depth ):
		result = DFS( startState, goalState, i )
		if result != None:
			return result
def main():
	
	result = BFS(startState,goalState)
	if(result==None):
		print("No solution")
	else:
		print("----------------------------------")
		print("BFS Search Result")
		print("Search states")
		for i in result:
			print(i)
		print("Goal state achieved in: ",len(result)," moves")
	
	result2 = DFS(startState,goalState,6)
	if(result2==None):
		print("No solution")
	else:
		print("----------------------------------")
		print("DFS Search Result")
		print("Search states")
		for i in result2:
			print(i)
		print("Goal state achieved in: ",len(result2)," moves")
	
	result3 = iterative_deepening(startState,goalState,5)
	if(result3==None):
		print("No solution")
	else:
		print("----------------------------------")
		print("IDS Search Result")
		print("Search states")
		for i in result3:
			print(i)
		print("Goal state achieved in: ",len(result3)," moves")
				
if __name__ == "__main__":
	main()