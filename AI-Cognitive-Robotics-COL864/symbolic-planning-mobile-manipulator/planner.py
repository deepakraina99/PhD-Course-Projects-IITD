from environment import *

## planning type: 0,1,2,3
# for Accelerated Forward Planning, use 0
# for Accelerated Backward Planning, use 1
# for Forward Planning, use 2
# for Backward Planning, use 3
planning_type = 1

# @deadline(120)
# Defining a action space
def getActionSpace(objects,pickableObjects,destinations,enclosures):
	actionSpace=[]
	actionSpace.extend([actions[0],obj] for obj in objects)
	actionSpace.extend([actions[1],pobj] for pobj in pickableObjects)
	actionSpace.extend([actions[2],dest] for dest in destinations)
	actionSpace.extend([actions[3],encl, status[0]] for encl in enclosures)
	actionSpace.extend([actions[3],encl, status[1]] for encl in enclosures)

	with open(goal_file, 'r') as handle:
		goals = json.load(handle)['goals']
	items_list = []
	for goal in goals:
		items_list.extend([goal['object'],goal['target']])
	items_list = list(set(items_list)) 
	# print('items:', items_list)
	# actionSpace = [x for x in actionSpace if x[1] in items_list]
	print('ActionSpace: ', actionSpace)
	return actionSpace

# a function to get goal constraints for backward planning
def getGoalConstraints(goal_file,i_state,items_list,planning_type):
	with open(goal_file, 'r') as handle:
		goals = json.load(handle)['goals']
	print('goals:',goals)

	goalConstraints = {}
	inside_list = []
	on_list=[]
	for goal in goals:
		object = goal['object']
		target = goal['target']
		doState = goal['state']
		if doState == 'close':
			doState = 'Close'
		if target:
			if target == 'fridge' or target == 'cupboard':
				inside_list.append((object,target))
				goalConstraints['inside']= inside_list
				goalConstraints['on'] = on_list
				goalConstraints[target] = 'open'
				goalConstraints['close'] = [target]
				if planning_type == 1:
					if target == 'fridge' and 'cupboard' in items_list:
						goalConstraints['cupboard'] = 'open'
					if target == 'cupboard' and 'fridge' in items_list:
						goalConstraints['fridge'] = 'open'


			elif target == 'box':
				inside_list.append((object,target))
				goalConstraints['inside']= inside_list
				goalConstraints['on'] = on_list
				goalConstraints[target] = 'open'
				# goalConstraints['fridge'] = 'Close'
				if planning_type == 1:
					if 'cupboard' in items_list:
						goalConstraints['cupboard'] = 'open'
					if 'fridge' in items_list:
						goalConstraints['fridge'] = 'open'
					goalConstraints['close'] = [target]
			else:
				on_list.append((object,target))
				goalConstraints['on'] = on_list
				goalConstraints['inside']= inside_list
				goalConstraints['close'] = [target]
				if planning_type == 1:
					if 'cupboard' in items_list:
						goalConstraints['cupboard'] = 'open'
					if 'fridge' in items_list:
						goalConstraints['fridge'] = 'open'
		else:
			goalConstraints[object]=doState
		goalConstraints['grabbed']=''
	return goalConstraints

# a functions to get essential items list for backward planning
def getItemsList(goal_file,iState):
	with open(goal_file, 'r') as handle:
		goals = json.load(handle)['goals']
	items_list = []

	for goal in goals:
		i=1
		#finding goal object location
		if iState['inside']: 
			for x in iState['inside']:
				if x[0] == goal['object'] and i==1:
					goal_obj_ini_loc = x[1]
					items_list.append(goal_obj_ini_loc)
					items_list.append(goal['target'])
					i+=1
				
		if iState['on']: 
			for x in iState['on']:
				if x[0] == goal['object'] and i==1:
					goal_obj_ini_loc = x[1]
					items_list.append(goal_obj_ini_loc)
					items_list.append(goal['target'])
					i+=1

	items_list = list(set(items_list)) 
	print('items_list:',items_list)
	return items_list

# functions to get possible actions for backward planning
def getPossibleActions(state):
	possible_actions = []
	if 'grabbed' in state.keys():
		if state['grabbed']!='':
			grabbed_obj = state['grabbed']
			possible_actions.append(['pick',grabbed_obj])
	if 'fridge' in state.keys():
		fridge_state = state['fridge']
		if fridge_state == 'open':
			possible_actions.append(['changeState','fridge','open'])
		else:
			possible_actions.append(['changeState','fridge','Close'])
	if 'cupboard' in state.keys():
		cupboard_state = state['cupboard']
		if cupboard_state == 'Close':
			possible_actions.append(['changeState','cupboard','Close'])
		else:
			possible_actions.append(['changeState','cupboard','open'])
	if 'inside' in state.keys():
		inside_list = state['inside']
		for x in inside_list:
			possible_actions.append(['drop',x[0],x[1]])
	if 'on' in state.keys():
		on_list = state['on']
		for x in on_list:
			possible_actions.append(['drop',x[0],x[1]])
	if 'close' in state.keys():
		close_list = state['close']
		for x in close_list:
			possible_actions.append(['moveTo',x])

	# print('possible_actions:', possible_actions)
	return possible_actions

def checkRepeatedState(c_state,alldict):
	# print('all_dict:',alldict)
	for id in alldict.keys():
		# print('keyid:',id)
		temp_state = alldict[id]['State']
		# print('tempstate:',temp_state)
		# print('cstate:',c_state)
		cond1 = temp_state['grabbed']==c_state['grabbed']
		cond2 = temp_state['fridge']==c_state['fridge']
		cond3 = temp_state['cupboard']==c_state['cupboard']
		cond4 = sorted(temp_state['inside'])==sorted(c_state['inside'])
		cond5 = sorted(temp_state['on'])==sorted(c_state['on'])
		cond6 = sorted(temp_state['close'])==sorted(c_state['close'])
		# print(cond1,cond2,cond3,cond4,cond5,cond6)
		all_cond = cond1 and cond2 and cond3 and cond4 and cond5 and cond6
		if all_cond:
			# print('Rejecting, state is already in tree with id:{}'.format(id))
			# print('')
			return True
		# else:
		# 	return False

def getPlan(planning_type):

	###########################FORWARD PLANNING#####################################
	if planning_type == 0:
		actionSpace = getActionSpace(objects,pickableObjects,destinations,enclosures)
		
		state = getCurrentState()
		# state = getWorldState(world_id)
		initial_state = state
		print('Initial State: ',initial_state)

		print('goal_file: ',goal_file)
		with open(goal_file, 'r') as handle:
			goals = json.load(handle)['goals']
		items_list = []
		for goal in goals:
			#finding goal object location
			if state['inside']: 
				for x in state['inside']:
					if x[0] == goal['object']:
						goal_obj_loc = x[1]
						items_list.append(goal_obj_loc)
						items_list.append(goal['target'])
				for x in state['on']:
					if x[0] == goal['object']:
						# goal_obj_loc = x[1]
						# items_list.append(goal_obj_loc)
						items_list.append(goal['object'])
			else:
				items_list.extend([goal['object'],goal['target']])
		items_list = list(set(items_list)) 
		print('items_list:',items_list)
		id=0
		treeDict = {0:{'parent':-1, 'action': "None", 'State': state, 'cost':0, 'depth': 1}}
		priority_queue = {0:1000000}
		closed_list=[]
		goalReached = False
		heuristics = True
		print('Finding plan, please wait...')
		while not goalReached:
			#consider the node with lowest cost
			priority_queue = {k: v for k, v in sorted(priority_queue.items(), key=lambda x: x[1])}
			# print('priority_queue: ',priority_queue)
			currentStateID = list(priority_queue.keys())[0]
			priority_queue.pop(currentStateID)
			# print('current state',currentStateID)
			# print('tree dict:',treeDict)
			state = treeDict[currentStateID]['State']
			if state['close']:
				items_list.extend(state['close'])
			# print('items_list',items_list) 
			items_list = list(set(items_list))
			# print('items_list',items_list) 
			#checking if goal has been reached
			if checkGoal(state):
				goalReached = True
				goalStateID = currentStateID
				print('Goal Reached !!!')
				print('Goal state: ', state)
				break
			else:
				closed_list.append(currentStateID)
				# print('closed_list:',closed_list)
				parent = currentStateID
				# print('parent: ',treeDict[parent])
				possible_actions = []
				tempActionSpace = actionSpace
				for action in tempActionSpace:
					isPossible = checkAction(state,action)
					if isPossible:
						possible_actions.append(action)
						# print(notVisited)
						##calculating cost
						cost_state = treeDict[parent]['cost']+ 1
						heuristic_cost = 1
						#Heuristics for accelerated plans:
						#1.Avoiding states achieved by actions of irrelevant objects
						if action[1] not in items_list:
							heuristic_cost = 50
						#2.Avoiding states obtained after repeatitive moveTo actions
						if action[0] == 'moveTo' and treeDict[parent]['action'][0] == 'moveTo':
							heuristic_cost = 50
						#3.Avoiding moving towards pickable objects when something is already grabbed
						exception_picks = [x for x in pickableObjects if x!='box']
						# print('exception:', exception_picks)
						if action[0] == 'moveTo' and treeDict[parent]['State']['grabbed']!='' and action[1] in exception_picks:
							heuristic_cost = 50
						#4.Avoiding consecutive changeState actions
						if action[0] == 'changeState' and treeDict[parent]['action'][0] == 'changeState':
							heuristic_cost = 50
						#5.Avoiding consecutive pick and drop
						if (action[0] == 'pick' and treeDict[parent]['action'][0] == 'drop') or \
						(action[0] == 'drop' and treeDict[parent]['action'][0] == 'pick'):
							heuristic_cost = 50
						#6.Avoiding actions more than max limit
						if cost_state > 25:
							heuristic_cost = 50

						if (heuristics):
							cost = cost_state + heuristic_cost
						else:
							cost = cost_state
						#add logic for repeated states here
						##
						newState = changeState(state,action)
						if not checkRepeatedState(newState,treeDict):
							id+=1
							# print('id:action:newStg:h:f::{}:{}:{}:{}:{}'.format(id,action,cost_state,heuristic_cost,cost))
							depthParent = treeDict[parent]['depth']
							treeDict.update({id:{'parent':parent, 'action':action, 'State': changeState(state,action), 'cost': cost_state, 'depth': depthParent + 1}})
							priority_queue.update({id:cost})
				# print('possible actions {} at state {}'.format(possible_actions,parent))
				# print('tree_Dic: ', treeDict)
				# print('')
			# print('Tree: ', treeDict)	
		
		##Branching factor
		print('goal state id:', goalStateID)
		numLeaves = goalStateID-1
		depthReached = treeDict[goalStateID]['depth']
		ABF = numLeaves/depthReached
		print('leaves:depth:average branching factor::{}:{}:{}'.format(numLeaves,depthReached,ABF))	

		## Backtracking to get actions
		actions_list = []
		lastState = goalStateID
		while not lastState == 0:
			stateID = lastState
			actions_list.insert(0,treeDict[stateID]['action'])
			lastState = treeDict[stateID]['parent']
		actions_list = [[x[0],x[1],'close'] if (x[0] == 'changeState' and x[2] == 'Close') else x for x in actions_list]
		print('Plan: ', actions_list)
		# return actions_list
	
	#################BACKWARD PLANNING: BREADTH FIRST SEARCH#####################
	elif planning_type == 1 or planning_type == 3:
		initial_state = getCurrentState()
		# initial_state = getWorldState(world_id)
		print('initial_state:',initial_state)
		# items_list = ['table2','fridge']
		items_list = getItemsList(goal_file,initial_state)
		print('items_list:',items_list)
		goalConstraints = getGoalConstraints(goal_file,initial_state,items_list,planning_type)
		print('goal_constraints: ',goalConstraints)

		initialReached = False
		currentState = goalConstraints
		treeDict = {0:{'parent':-1, 'action': "None", 'State': currentState, 'depth': 1}}
		notVisited = [0]
		id=0
		lastStateID = 0
		print('Finding plan, please wait...')

		while not initialReached:
			if checkInitial(initial_state,currentState,planning_type):
				initialReached = True
				print('initial reached !!')
				break
			else:
				# print('notVisited:',notVisited)
				currentStateID = notVisited[0]
				# print('current state ID:',currentStateID)
				currentState = treeDict[currentStateID]['State']
				notVisited.pop(0)
				# print('parent: ',treeDict[currentStateID])
				list_actions = getPossibleActions(currentState)
				valid_actions=[]
				for action in list_actions:
					isValid = checkActionBkwd(currentState,action,planning_type)
					if isValid:
						valid_actions.append(action)
						prevState = changeStateBkwd(currentState,action,initial_state,items_list,planning_type)
						# if not checkRepeatedState(prevState,treeDict):
						id+=1
						# print('id:action:newState::{}:{}:{}'.format(id,action,prevState))
						# print('')
						depthParent = treeDict[currentStateID]['depth']
						treeDict.update({id:{'parent':currentStateID, 'action':action, 'State':prevState, 'depth': depthParent + 1}})
						if checkInitial(initial_state,prevState,planning_type):
							initialReached = True
							print('initial reached !!')
							lastStateID = id
							break
						notVisited.append(id)
						# print('Stop')
						# print('')

		##Branching factor
		print('goal state id:', lastStateID)
		numLeaves = lastStateID-1
		depthReached = treeDict[lastStateID]['depth']
		ABF = numLeaves/depthReached
		print('leaves:depth:average branching factor::{}:{}:{}'.format(numLeaves,depthReached,ABF))	

		## Backtracking to get actions
		actions_list = []
		# print(lastStateID)
		while not lastStateID == 0:
			stateID = lastStateID
			# print(treeDict)
			actions_list.append(treeDict[stateID]['action'])
			lastStateID = treeDict[stateID]['parent']

		pick_indexes = [i for i in range(len(actions_list)) if actions_list[i][0]=='pick' or actions_list[i][0]=='changeState']
		# print(pick_indexes)
		i=0
		for idx in pick_indexes:
			actions_list.insert(idx+i,['moveTo',actions_list[idx+i][1]])
			i+=1
		actions_list = [[x[0],x[2]] if x[0] == 'drop' else x for x in actions_list]
		actions_list = [[x[0],x[1],'close'] if (x[0] == 'changeState' and x[2] == 'Close') else x for x in actions_list]
		print('Plan: ', actions_list)
		# return actions_list

	####################FORWARD PLANNING: UNIFORM COST SEARCH####################
	elif planning_type == 2:
		actionSpace = getActionSpace(objects,pickableObjects,destinations,enclosures)
		
		state = getCurrentState()
		# state = getWorldState(world_id)
		initial_state = state
		print('Initial State: ',initial_state)

		print('goal_file: ',goal_file)
		with open(goal_file, 'r') as handle:
			goals = json.load(handle)['goals']
		items_list = []
		for goal in goals:
			#finding goal object location
			if state['inside']: 
				for x in state['inside']:
					if x[0] == goal['object']:
						goal_obj_loc = x[1]
						items_list.append(goal_obj_loc)
						items_list.append(goal['target'])
				for x in state['on']:
					if x[0] == goal['object']:
						items_list.append(goal['object'])
			else:
				items_list.extend([goal['object'],goal['target']])
		items_list = list(set(items_list)) 
		# print('items_list:',items_list)
		id=0
		treeDict = {0:{'parent':-1, 'action': "None", 'State': state, 'cost':0, 'depth': 1}}
		priority_queue = {0:1000000}
		closed_list=[]
		goalReached = False
		heuristics = True
		print('Finding plan, please wait...')
		while not goalReached:
			#consider the node with lowest cost
			priority_queue = {k: v for k, v in sorted(priority_queue.items(), key=lambda x: x[1])}
			# print('priority_queue: ',priority_queue)
			currentStateID = list(priority_queue.keys())[0]
			priority_queue.pop(currentStateID)
			# print('current state',currentStateID)
			state = treeDict[currentStateID]['State']
			if state['close']:
				items_list.extend(state['close'])
			items_list = list(set(items_list))
			# print('items_list',items_list) 
			#checking if goal has been reached
			if checkGoal(state):
				goalReached = True
				goalStateID = currentStateID
				print('Goal Reached !!!')
				print('Goal state: ', state)
				break
			else:
				closed_list.append(currentStateID)
				# print('closed_list:',closed_list)
				parent = currentStateID
				# print('parent: ',treeDict[parent])
				possible_actions = []
				tempActionSpace = actionSpace
				for action in tempActionSpace:
					isPossible = checkAction(state,action)
					if isPossible:
						possible_actions.append(action)
						# print(notVisited)
						##calculating cost
						cost_state = treeDict[parent]['cost']+ 1
						heuristic_cost = 1
						#Heuristics for accelerated plans:
						#1.Avoiding states achieved by actions of irrelevant objects
						# if action[1] not in items_list:
							# heuristic_cost = 50
						# #2.Avoiding states obtained after repeatitive moveTo actions
						# if action[0] == 'moveTo' and treeDict[parent]['action'][0] == 'moveTo':
						# 	heuristic_cost = 50
						# #3.Avoiding moving towards pickable objects when something is already grabbed
						# exception_picks = [x for x in pickableObjects if x!='box']
						# # print('exception:', exception_picks)
						# if action[0] == 'moveTo' and treeDict[parent]['State']['grabbed']!='' and action[1] in exception_picks:
						# 	heuristic_cost = 50
						# #4.Avoiding consecutive changeState actions
						# if action[0] == 'changeState' and treeDict[parent]['action'][0] == 'changeState':
						# 	heuristic_cost = 50
						# #5.Avoiding consecutive pick and drop
						# if (action[0] == 'pick' and treeDict[parent]['action'][0] == 'drop') or \
						# (action[0] == 'drop' and treeDict[parent]['action'][0] == 'pick'):
						# 	heuristic_cost = 50
						# #6.Avoiding actions more than max limit
						# if cost_state > 16:
						# 	heuristic_cost = 50

						if (heuristics):
							cost = cost_state + heuristic_cost
						else:
							cost = cost_state
						#logic for repeated states here
						newState = changeState(state,action)
						if not checkRepeatedState(newState,treeDict):
							id+=1
							# print('id:action:newstate:g:h:f::{}:{}:{}:{}:{}:{}'.format(id,action,newState,cost_state,heuristic_cost,cost))
							# print('')
							depthParent = treeDict[parent]['depth']
							treeDict.update({id:{'parent':parent, 'action':action, 'State': changeState(state,action), 'cost': cost_state, 'depth': depthParent+1}})
							priority_queue.update({id:cost})
				# print('possible actions {} at state {}'.format(possible_actions,parent))
				# print('tree_Dic: ', treeDict)
				# print('Stop')
				
		## Branching factor
		print('goal state id:', goalStateID)
		numLeaves = goalStateID-1
		depthReached = treeDict[goalStateID]['depth']
		ABF = numLeaves/depthReached
		print('leaves:depth:average branching factor::{}:{}:{}'.format(numLeaves,depthReached,ABF))	
		
		## Backtracking to get actions
		actions_list = []
		lastState = goalStateID
		while not lastState == 0:
			stateID = lastState
			actions_list.insert(0,treeDict[stateID]['action'])
			lastState = treeDict[stateID]['parent']
		actions_list = [[x[0],x[1],'close'] if (x[0] == 'changeState' and x[2] == 'Close') else x for x in actions_list]
		print('Plan: ', actions_list)
	
	end = time.time()
	print('Time taken: {} seconds'.format(end - start))
	return actions_list

# def getPlan():
#	 #######################################
#	 ######## Insert your code here ########
#	 #######################################
#	 return [["moveTo", "fridge"], \
#				["changeState", "fridge", "open"], \
#				["moveTo", "apple"], \
#				["pick", "apple"], \
#				["moveTo", "fridge"], \
#				["drop", "fridge"], \
#				["moveTo", "orange"], \
#				["pick", "orange"], \
#				["moveTo", "fridge"], \
#				["drop", "fridge"], \
#				["moveTo", "banana"], \
#				["pick", "banana"], \
#				["moveTo", "fridge"], \
#				["drop", "fridge"], \
#				["changeState", "fridge", "close"], \
#				]
   
# Execute function takes in a plan as input and returns if goal constraints 
# are valid and the final state after plan execution
# getPlan(planning_type)
import os
import shutil
name = os.getcwd().replace('\\', '/').split('/')[-1]

if args.input == 'part1':
    testOutput = 'testLogs/'+args.input+'/errors.txt'
    testResult = 'testLogs/'+args.input+'/result.txt'
    errors = open(testOutput, 'w+')
    result = open(testResult, 'w+')

all_worlds = {
    0: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'table2'), ('orange', 'table2'), ('banana', 'table2'), ('tray', 'table'), ('tray2', 'table2')], 'close': []},
    1: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('tray', 'table'), ('tray2', 'table2')], 'close': []},
    2: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'table2'), ('orange', 'table'), ('tray', 'table'), ('tray2', 'table2')], 'close': []},
    3: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [('orange', 'cupboard'), ('banana', 'cupboard')], 'on': [('tray', 'table'), ('tray2', 'table2')], 'close': []},
    4: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [('apple', 'fridge'), ('orange', 'fridge'), ('banana', 'fridge')], 'on': [('tray', 'table'), ('tray2', 'table2')], 'close': []},
    5: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'cupboard'), ('orange', 'cupboard'), ('banana', 'cupboard'), ('tray', 'table'), ('tray2', 'table2')], 'close': []},
    6: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'table'), ('orange', 'table'), ('banana', 'table'), ('tray', 'table'), ('tray2', 'table2')], 'close': []},
    7: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'table2'), ('orange', 'table2'), ('banana', 'table2'), ('tray', 'table'), ('tray2', 'table2')], 'close': []},
    8: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('tray', 'table'), ('tray2', 'table2')], 'close': []},
    9: {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'table'), ('tray', 'table'), ('tray2', 'table2')], 'close': []}
}

plans = {
    0: [["moveTo", "fridge"], \
               ["changeState", "fridge", "open"], \
               ["moveTo", "apple"], \
               ["pick", "apple"], \
               ["moveTo", "fridge"], \
               ["drop", "fridge"], \
               ["moveTo", "orange"], \
               ["pick", "orange"], \
               ["moveTo", "fridge"], \
               ["drop", "fridge"], \
               ["moveTo", "banana"], \
               ["pick", "banana"], \
               ["moveTo", "fridge"], \
               ["drop", "fridge"], \
               ["changeState", "fridge", "close"], \
               ], # fruits in fridge
    1: [["moveTo", "apple"], \
               ["pick", "apple"], \
               ["moveTo", "table"], \
               ["drop", "table"], \
               ], # apple on table
    2: [["moveTo", "apple"], \
               ["pick", "apple"], \
               ["moveTo", "box"], \
               ["drop", "box"], \
               ["moveTo", "orange"], \
               ["pick", "orange"], \
               ["moveTo", "box"], \
               ["drop", "box"], \
               ["moveTo", "banana"], \
               ["pick", "banana"], \
               ["moveTo", "box"], \
               ["drop", "box"], \
               ], # fruits in box
    3:  [["moveTo", "fridge"], \
               ["changeState", "fridge", "open"], \
               ["moveTo", "apple"], \
               ["pick", "apple"], \
               ["moveTo", "fridge"], \
               ["drop", "fridge"], \
               ["changeState", "fridge", "close"], \
               ] # apple in fridge
}

def checkGoalWorking(state, goal_id):
    if goal_id == 0:
        return ('apple', 'table') in state['on']
    elif goal_id == 1:
        return (('apple', 'box') in state['inside'] and 
        ('orange', 'box') in state['inside'] and
        ('banana', 'box') in state['inside'])
    elif goal_id == 2:
        return (('apple', 'fridge') in state['inside'])
    elif goal_id == 3:
        return (('apple', 'fridge') in state['inside'] and 
        ('orange', 'fridge') in state['inside'] and 
        ('banana', 'fridge') in state['inside'] and 
        state['fridge'] == 'Close')
    elif goal_id == 4:
        return (('apple', 'fridge') in state['inside'] and 
        ('orange', 'cupboard') in state['inside'] and 
        ('banana', 'box') in state['inside'] and 
        state['fridge'] == 'Close' and state['cupboard'] == 'Close')

def checkActionWorking(state, action):
    if action[0] == 'moveTo':
        return True
    elif action[0] == 'pick':
        return action[1] in state['close'] and action[1] not in ['fridge', 'table', 'table2']
    elif action[0] == 'drop':
        return not (action[0] == action[1] or \
            action[1] not in ['table', 'table2', 'box', 'fridge', 'tray', 'tray2'] or \
            (action[1] in enclosures and state[action[1]] =='Close') or \
            action[1] not in state['close'])
    elif action[0] == 'changeState':
        return not (action[1] not in enclosures or \
            action[1] not in state['close'] or \
            state[action[1]] == action[2])
    elif action[0] == 'pushTo':
        return action[1] in state['close'] and action[1] != action[2]

def changeStateWorking(state1, action):
    state = deepcopy(state1)
    if action[0] == 'moveTo':
        state['close'] = [action[1]]
    elif action[0] == 'pick':
        state['grabbed'] = action[1]
    elif action[0] == 'drop':
        obj = state['grabbed']
        state['grabbed'] = ''
        if action[1] in ['box', 'fridge']:
            state['inside'].append((obj, action[1]))
        else:
            state['on'].append((obj, action[1]))
    elif action[0] == 'changeState':
        state['fridge'] = 'Close' if state['fridge'] == 'Open' else 'Open'
    elif action[0] == 'pushTo':
        state['close'] = [action[2]]
    return state

def checkStateEquality(statePred, stateTrue):
    return (statePred['grabbed'] == stateTrue['grabbed'] and
        statePred['fridge'] == stateTrue['fridge'] and
        statePred['cupboard'] == stateTrue['cupboard'] and
        set(statePred['inside']).issubset(set(stateTrue['inside'])) and
        set(statePred['on']).issubset(set(stateTrue['on'])) and
        set(stateTrue['close']).issubset(set(statePred['close'])))

def testCheckAction():
    total_tests = 0; incorrect = 0
    errors.writelines(["\n\n#### Testing Check Action ####\n\n"])
    result.writelines(["\n\n#### Testing Check Action ####\n\n"])
    for worldID in range(5):
        for planID in range(4):
            for goal_id in range(4):
                state = all_worlds[worldID]
                plan = plans[planID]
                for action in plan:
                    total_tests += 1
                    if checkAction(state, action) and not checkActionWorking(state, action):
                        errors.writelines(["\nERROR: planner says incorrect action for a valid action\n"])
                        errors.writelines(["State\n", state, "\nAction\n", action])
                        incorrect += 1
                    elif not checkActionWorking(state, action) and checkAction(state, action):
                        errors.writelines(["\nERROR: planner says correct action for an invalid action\n"])
                        errors.writelines(["State\n", state, "\nAction\n", action])
                        incorrect += 1
                        break
                    state = changeStateWorking(state, action) 
    result.writelines(["Total tests\n", str(total_tests), "\nTotal incorrect\n", \
        str(incorrect), "\nPercentage correct\n", str(100.0*(total_tests-incorrect)/total_tests)])

def testChangeState():
    total_tests = 0; incorrect = 0
    errors.writelines(["\n\n#### Testing Change State ####\n\n"])
    result.writelines(["\n\n#### Testing Change State ####\n\n"])
    for worldID in range(5):
        for planID in range(4):
            for goal_id in range(4):
                state = all_worlds[worldID]
                plan = plans[planID]
                for action in plan:
                    total_tests += 1
                    if checkAction(state, action):
                        statePred = changeState(state, action) 
                        stateTrue = changeStateWorking(state, action)
                        if not checkStateEquality(statePred, stateTrue):
                            errors.writelines(["\nERROR: incorrect final state\n", str(statePred), '\nTrue state\n', str(stateTrue)])
                            errors.writelines(["\nOriginal state\n", str(state)])
                            errors.writelines(["\nOriginal action\n", str(action), '\n'])
                            incorrect += 1
                        state = statePred
                    else:
                        break
    result.writelines(["Total tests\n", str(total_tests), "\nTotal incorrect\n", \
        str(incorrect), "\nPercentage correct\n", str(100.0*(total_tests-incorrect)/total_tests)])

def checkPlan(test):
    testOutput = 'testLogs/'+args.input+'/errors_G'+args.goal.split('.')[1][-1]+'_W'+args.world.split('.')[1][-1]+'.txt'
    testResult = 'testLogs/'+args.input+'/result_G'+args.goal.split('.')[1][-1]+'_W'+args.world.split('.')[1][-1]+'.txt'
    errors = open(testOutput, 'w+')
    result = open(testResult, 'w+')
    if test == 'part2':
        errors.writelines(["\n\n#### Checking forward search ####\n"])
        result.writelines(["\n\n#### Checking forward search ####\n"])
    elif test == 'part3':
        errors.writelines(["\n\n#### Checking backward search ####\n"])
        result.writelines(["\n\n#### Checking backward search ####\n"])
    elif test == 'part4' or test == 'part5':
        errors.writelines(["\n\n#### Checking accelerated search ####\n"])
        result.writelines(["\n\n#### Checking accelerated search ####\n"])
    start = time.time(); print(0)
    try:
        if test == 'part2':
            plan = getPlan(2) ####
        elif test == 'part3':
            plan = getPlan(3) ####
        else:
            plan = getPlan(0) ####
        state = getCurrentState()
        result.writelines(["\n\nInitial State: ", str(state)])
        errors.writelines(["\n\nInitial State: ", str(state)])
        errors.writelines(["\n\nPlan\n", str(plan)])
        result.writelines(["\n\nPlan\n", str(plan)])
        result.writelines(["\nPlan length: ", str(len(plan))])
        result.writelines(["\nTime: ", str(time.time() - start)])
    except Exception as e:
        errors.writelines(["\n\nERROR:\n", str(e), "\n"])
    print(time.time()-start)
    try:
        res, state = execute(plan)
        result.writelines(["\n\nFinal State: ", str(state)])
        result.writelines(["\n\nSymbolic Result: ", str(checkGoalWorking(state, int(args.goal.split('.')[1][-1])))])
        result.writelines(["\n\nExecution Result: ", str(res or checkGoalWorking(state, int(args.goal.split('.')[1][-1])))])
        errors.writelines(["\n\nFinal State\n", str(state)])
    except Exception as e:
        errors.writelines(["\n\nERROR WHILE EXECUTING PLAN:\n", str(e), "\n"])
    errors.close(); result.close()

if __name__ == '__main__':
    if args.input == 'part1':
        testCheckAction()
        testChangeState()
        errors.close(); result.close()
    else:
        checkPlan(args.input)