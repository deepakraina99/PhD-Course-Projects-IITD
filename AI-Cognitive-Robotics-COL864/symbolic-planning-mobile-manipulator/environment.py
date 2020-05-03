from husky_ur5 import *
from copy import deepcopy
import json
import time
import random

start = time.time()
# goal_file = "jsons/home_goals/goal3.json"
goal_file = args.goal
# world_id = 0

## FINAL TESTING:
# AFP: Done, ABP: Done, FP: Done, BP: Done

def getWorldState(id):
	if id==0: state = {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('apple', 'table2'), ('orange', 'table2'), ('banana', 'table2'), ('banana', 'tray2'), ('tray', 'table'), ('tray2', 'table2')], 'close': []}
	elif id==1: state = {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [], 'on': [('tray', 'table'), ('tray2', 'table2')], 'close': []}
	elif id==2: state = {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [('banana', 'cupboard')], 'on': [('apple', 'table2'), ('orange', 'table'), ('tray', 'table'), ('tray2', 'table2')], 'close': []}
	elif id==3: state = {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [('apple', 'cupboard'), ('orange', 'cupboard'), ('banana', 'cupboard')], 'on': [('tray', 'table'), ('tray2', 'table2')], 'close': []}
	elif id==4: state = {'grabbed': '', 'fridge': 'Close', 'cupboard': 'Close', 'inside': [('apple', 'fridge'), ('orange', 'fridge'), ('banana', 'fridge')], 'on': [('tray', 'table'), ('tray2', 'table2')], 'close': []}
	return state

state = getCurrentState()
# state = getWorldState(world_id)
print('state:',state)

objects = ['apple', 'orange', 'banana', 'table', 'table2', 'box', 'fridge', 'tray', 'tray2', 'cupboard']
enclosures = ['fridge', 'cupboard']
pickableObjects = ['apple','banana','orange','tray','tray2']
destinations = ['fridge','cupboard','box','table','table2','tray','tray2']
status = ['open','Close']

actions = ['moveTo', 'pick', 'drop', 'changeState', 'pushTo']

########################FORWARD PLANNING FUNCTIONS################################
# A checker for action feasibility
def checkAction(state, action):
	actionType = action[0]

	# Check if action is possible for state
	if actionType == 'moveTo':
		object = action[1]
		if not (object in state['close'] or object in state['grabbed']):
			return True
		else:
			return False

	if actionType == 'pick':
		object = action[1]
		if state['grabbed']=='' and object in state['close']:
			#check if object inside enclosure
			object_location = [x[1] for x in state['inside'] if x[0]==object]
			# object_location = object_location[0]
			if len(object_location)!=0:
				object_location = object_location[0]
				if object_location == 'fridge' or object_location == 'cupboard':
					if state[object_location] == 'open':
						return True
					else:
						return False
			else:
				return True
		else:
			return False
	
	if actionType == 'drop':
		destination= action[1]
		if state['grabbed']!='' and destination in state['close']:
			if destination == 'fridge' or destination == 'cupboard':
				if state[destination] == 'open':
					return True
				else:
					return False
			else:
				return True
		else:
			return False

	if actionType == 'changeState':
		object = action[1]
		newState = action[2]
		if state['grabbed']=='' and object in state['close']:
			if newState == 'open':
				if state[object] == 'Close': 
					return True
				elif state[object] == 'open':
					return False
			elif newState == 'Close':
				if state[object] == 'open': 
					return True
				elif state[object] == 'Close':
					return False
		else:
			return False

	if actionType == 'pushTo':
		object = action[1]
		destination = action[2]
		if object in state['close']:
			return True
		else:
			return False

# An approximate environment model
def changeState(state1, action):
	state = deepcopy(state1)	
	actionType = action[0]
	close_list = []
	inside_list  = state['inside']
	on_list = state['on']
	# global inside_list, on_list
	if actionType == 'moveTo':
		location = action[1]
		if (location == 'fridge' or location == 'cupboard') and state[location] == 'open':
			all_objs_encls = [x[0] for x in state['inside'] if x[1] == location]
			close_list.append(location)
			close_list.extend(all_objs_encls)
		else:
			close_list.append(location)
		state['close'] = close_list

	if actionType == 'pick':
		object = action[1]
		state['grabbed'] = object
		on_list = [x for x in on_list if x[0] != object]
		state['on'] = on_list
		inside_list = [x for x in inside_list if x[0] != object]
		state['inside'] = inside_list


	if actionType == 'drop':
		destination = action[1]
		grabbedObject = state['grabbed']
		state['grabbed'] = ''
		state['close'] = close_list
		if destination  == 'fridge' or destination == 'cupboard' or destination == 'box':
			inside_list.append((grabbedObject,destination))
			state['inside'] = inside_list
			on_list = [x for x in on_list if x[0] != grabbedObject]
			state['on'] = on_list
			all_objs_encls = [x[0] for x in state['inside'] if x[1] == destination]
			close_list.append(destination)
			close_list.extend(all_objs_encls)
		else:
			on_list = [x for x in on_list if x[0] != grabbedObject]
			on_list.append((grabbedObject,destination))
			state['on'] = on_list
			close_list.extend([destination,grabbedObject])


	if actionType == 'changeState':
		object = action[1]
		newState = action[2]
		state[object] = newState
		if newState == 'open':
			all_objs_encls = [x[0] for x in state['inside'] if x[1] == object]
			close_list.extend(all_objs_encls)
		close_list.append(object)
		state['close'] = close_list

		
	if actionType == 'pushTo':
		object = action[1]
		destination = action[2]
		close_list.extend([object,destination])
		state['close'] = close_list

	return state

# An approximate goal checker
def checkGoal(state):

	with open(goal_file, 'r') as handle:
		goals = json.load(handle)['goals']
	# print('goals:',goals)

	checkGoalList=[]
	for goal in goals:
		object = goal['object']
		target = goal['target']
		doState = goal['state']
		#to correct case-sensitivity
		if doState == 'close':
			doState = 'Close'
		if target:
			if target == 'fridge' or target == 'cupboard' or target == 'box':
				checkGoalList.append((object,target) in state['inside'])
			else:
				checkGoalList.append((object,target) in state['on'])
		else:
			checkGoalList.append(state[object] == doState)
	# print(checkGoalList)
	IsGoalAttained = all(x==True for x in checkGoalList)
	return IsGoalAttained

########################BACKWARD PLANNING FUNCTIONS##############################
# A checker for action feasibility
def checkActionBkwd(state,action,planner_type):
	actionType = action[0]
	if actionType == 'moveTo':
		object = action[1]
		if object in state['close']:
			return True
		else:
			return False

	if actionType == 'drop':
		object = action[1]
		destination = action[2]
		encls = ['fridge','cupboard','box']
		on_dest,inside_dest=[],[]
		if destination in encls:	
			inside_dest = [x for x in state['inside']]
			inside_dest = list(set(inside_dest))
		else:
			on_dest = [x for x in state['on']]
			on_dest = list(set(on_dest))

		if 'grabbed' in state.keys():
			condition = ((object,destination) in on_dest or ((object,destination) in inside_dest and state[destination]=='open')) and state['grabbed']==''
		else:
			condition = ((object,destination) in on_dest or ((object,destination) in inside_dest and state[destination]=='open'))
		
		if condition:
			return True
		else:
			return False

	if actionType == 'pick':
		object = action[1]
		destinations = ['fridge','cupboard','box','table','table2','tray','tray2']
		close_list = state['close']
		if planner_type == 1:
			if state['close']:
				for x in close_list:
					if x in destinations:
						closest_station = x
					else:
						closest_station = False
					if state['grabbed'] == object and closest_station:
						if closest_station == 'fridge' or closest_station=='cupboard':
							if state[closest_station] == 'open':
								return True
							else:
								return False
						else:
							return True
					else:
						return False
			elif state['grabbed'] == object:
				return True
			else:
				return False
		elif planner_type == 3:
			if state['close']:
				for x in close_list:
					if x in destinations:
						closest_station = x
					else:
						closest_station = False
					if state['grabbed'] == object and closest_station:
						if closest_station == 'fridge' or closest_station=='cupboard':
							if state[closest_station] == 'open':
								return True
							else:
								return False
						else:
							return True
					else:
						return False
			# elif state['grabbed'] == object:
			# 	return True
			else:
				return False

	if actionType == 'changeState':
		encls = action[1]
		doState = action[2]
		if planner_type == 1:
			if state['close']:
				if state[encls]==doState and state['grabbed']=='' and encls in state['close']:
					return True
				else:
					return False
			elif state[encls]==doState and state['grabbed']=='':
				return True
		else:
			if state[encls]==doState and state['grabbed']=='' and encls in state['close']:
				return True
			else:
				return False	

		if actionType == 'pushTo':
			object = action[1]
			destination = action[2]
			if object and destination in state['close']:
				return True
			else:
				return False

# An approximate environment model
def changeStateBkwd(state1,action,iState,items_list,planner_type):

	state = deepcopy(state1)
	actionType = action[0]
	on_list = []
	inside_list = []
	close_list = []
	if actionType == 'moveTo':
		object = action[1]
		# close_list = state['close']
		if planner_type == 3:
			destinations = ['fridge','cupboard','box','table','table2','']
			
			# if object in destinations:
			#     close_list = [x for x in destinations if x!=object] 
			close_list = [x for x in destinations if x!=object] 
			# print(close_list)                  
			# state['close'] = close_list
			weight = [1 if (x=='' or x=='table2') else 1 for x in  close_list]
			# print('weight',weight)
			total_weight = sum(weight)
			weight = [x/total_weight for x in weight]
			close_list = random.choices(close_list,weight)
			close_object = close_list[0]
			if close_object == '':
				close_list= []
			elif  close_object == 'fridge' or close_object == 'cupboard' or close_object=='box':
				state[close_object] = 'open'
			# print(close_list)  
		else:
			grabbedObj = state['grabbed']

			if object in items_list and state['grabbed']=='':
				close_list = [x for x in items_list if x!=object]	
				close_list = [random.choice(close_list)]
			elif grabbedObj:
				if iState['inside']: 
					for x in iState['inside']:
						if x[0] == grabbedObj:
							goal_obj_ini_loc = x[1]
							close_list = [goal_obj_ini_loc]

						
				if iState['on']: 
					for x in iState['on']:
						if x[0] == grabbedObj:
							goal_obj_ini_loc = x[1]
							close_list = [goal_obj_ini_loc]

		state['close'] = close_list

	if actionType == 'drop':
		object = action[1]
		destination = action[2]
		# close_list = state['close']
		enclosures = ['fridge','cupboard','box']
		if destination in enclosures:
			inside_list = state['inside']
			inside_list = [x for x in inside_list if x[0]!=object]
			state['inside'] = inside_list
		else:
			on_list = state['on']
			on_list = [x for x in on_list if x[0]!=object]
			state['on'] = on_list
		state['grabbed'] = object
		close_list = [destination]
		state['close'] = close_list

	if actionType == 'changeState':
		encls = action[1]
		doState = action[2]
		if doState == 'open':
			state[encls]='Close'
		else:
			state[encls]='open'

	if actionType == 'pick':
		object = action[1]
		close_list = state['close']
		destinations = ['fridge','cupboard','box','table','table2','tray2','tray']
		if state['close']:
			for x in close_list:
				if x in destinations:
					location = x
			state['grabbed'] = ''
			enclosures = ['fridge','cupboard','box']
			if location in enclosures:
				inside_list = state['inside']
				inside_list.extend([(object,location)])
				state['inside'] = inside_list
			else:
				on_list = state['on']
				on_list.extend([(object,location)])
				state['on'] = on_list
		else:
			state['grabbed'] = ''

			# close_list.append(location)
		if planner_type == 3:
			state['close'] = [location]
	if actionType == 'pushTo':
		object = action[1]
		destination = action[2]
		close_list = state['close']
		close_list = [x for x in close_list if x!=object]
		state['close'] = close_list
	return state  

# An approximate initial state checker
def checkInitial(i_state,c_state,planner_type):
	satisfiedConstraints = []
	# print('i_state:',i_state)
	# print('c_state:',c_state)
	if planner_type == 1:
		for key in i_state.keys():
			if key in c_state.keys():
				if key=='fridge' or key=='cupboard' or key=='grabbed':
					satisfiedConstraints.append(c_state[key] == i_state[key]) 
				elif key!='close':
					for c_value in c_state[key]:
						checkPresent = c_value in i_state[key]
						satisfiedConstraints.append(checkPresent)
		# print('constraints satisfied:', satisfiedConstraints)
	else:
		for key in i_state.keys():
			if key in c_state.keys():
				if key=='fridge' or key=='cupboard' or key=='grabbed':
					satisfiedConstraints.append(c_state[key] == i_state[key]) 
				else:
					for c_value in c_state[key]:
						checkPresent = c_value in i_state[key]
						satisfiedConstraints.append(checkPresent)
		# print('constraints satisfied:', satisfiedConstraints)
	IsInitialReached = all(x==True for x in satisfiedConstraints)
	return IsInitialReached  
