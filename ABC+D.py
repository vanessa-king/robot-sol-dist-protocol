###### USER INPUT ######

###1. Select plate type
container_choice = "full_alumina" # full_alumina, half_alumina, or cups. 
								   # Note: half_alumina can't be used to make a 2D symmetric gradient or parallelogram.

###2. Select Pipettes currently loaded in robot
current_pipettes = [10,50] #300, 50 or 10. First entry = Left mount, second entry = Right mount.

###3. Solution Distributions 
#Volumes in ul. 'x' direction is to the right, 'y' direction is down.
#Fill in for number of solutions desired.
#Examples: 
    #Constant volume: [50]
    #Checkerboard solution, constant volume: [5, "odd"] which gives-->  |  5   5   5|   or [5, "even"] which gives--> |5   5   5  |
    #                                                                   |5   5   5  |                                 |  5   5   5|
    #                                                                   |  5   5   5|                                 |5   5   5  |
    #                                                                   |5   5   5  |                                 |  5   5   5| 
    #1D increasing gradient: [0, 50, 'x']
    #1D decreasing gradient: [50, 0, 'x']     
    #2D symettric gradient : [100, 0, '2D', 'symm']  which gives --> |100	   50|
    #												                 |   	     |	
    #												                 |50        0|
    #
    #For a 2D 'parallelogram' distribution: [100, 0, '2D', -1, 1] which gives --> |       100| and ... 1, -1] gives -->|100       | 
    #                                                                             |          |                         |          |
    #                                                                             |0         |                         |         0|
    #Not using a solution or the precipitator: [] 

solution_A = [8,1, 'x']
solution_B = [8,1, 'x']
solution_C = []
solution_D = []
precipitator = []


##Pipette Settings##

#Minimum Volume
P300_min_volume = 51 #ul
P50_min_volume = 11 #ul

#Dispense rate
P300_dispense_rate = 300 #ul/s
P50_dispense_rate = 75 #ul/s
P10_dispense_rate = 100 #ul/s

#Small volume condition (is the volume less than or equal to this value?)
small_condition = 6 #ul

###### END OF USER INPUT #######






###Settings
from opentrons import containers, instruments, robot, labware
from opentrons.data_storage import database
from sqlite3 import IntegrityError
import math


#Creating P50 Tiprack
try:
    custom_container = labware.create(
    'tiprack-Fisher200ul',           # name of your container. For a tiprack, must start with 'tiprack'
    grid=(12, 8),           # specify amount of (columns, rows)
    spacing=(8.5,8.5),      # distances (mm) between each (column, row)
    diameter=6.0,
    depth=60)              # depth (mm) of each tip on the rack
except IntegrityError:
    pass

#Creating aluminum plate container
try:
    custom_container = labware.create(
    'full_alumina',           # name of your container
    grid=(8, 8),           # specify amount of (columns, rows)
    spacing=(9.5,12),      # distances (mm) between each (column, row)
    diameter=0.5,            # diameter (mm) of each well on the plate
    depth=25)              # depth (mm) of each well on the plate
except IntegrityError:
    pass

#Creating half aluminum plate container.
try:
    custom_container = labware.create(
    'half_alumina_plate',  # name of your container
    grid=(4, 8),           # specify amount of (columns, rows)
    spacing=(9.5,12),      # distances (mm) between each (column, row)
    diameter=0.5,            # diameter (mm) of each well on the plate
    depth=25)              # depth (mm) of each well on the plate
except IntegrityError:
    pass

#Creating metal cups container. PART 1/4   
try:
    custom_container = labware.create(
    'metal_cups_part1',           # name of your container
    grid=(2, 8),           # specify amount of (columns, rows)
    spacing=(2,2),      # distances (mm) between each (column, row)
    diameter=7.4,            # diameter (mm) of each well on the plate
    depth=12.80)              # depth (mm) of each well on the plate
except IntegrityError:
    pass

#Creating metal cups container. PART 2/4   
try:
    custom_container = labware.create(
    'metal_cups_part2',           # name of your container
    grid=(2, 8),           # specify amount of (columns, rows)
    spacing=(2,2),      # distances (mm) between each (column, row)
    diameter=7.4,            # diameter (mm) of each well on the plate
    depth=12.80)              # depth (mm) of each well on the plate
except IntegrityError:
    pass

#Creating metal cups container. PART 3/4   
try:
    custom_container = labware.create(
    'metal_cups_part3',           # name of your container
    grid=(2, 8),           # specify amount of (columns, rows)
    spacing=(2,2),      # distances (mm) between each (column, row)
    diameter=7.4,            # diameter (mm) of each well on the plate
    depth=12.80)              # depth (mm) of each well on the plate
except IntegrityError:
    pass

#Creating metal cups container. PART 4/4   
try:
    custom_container = labware.create(
    'metal_cups_part4',           # name of your container
    grid=(2, 8),           # specify amount of (columns, rows)
    spacing=(2,2),      # distances (mm) between each (column, row)
    diameter=7.4,            # diameter (mm) of each well on the plate
    depth=12.80)              # depth (mm) of each well on the plate
except IntegrityError:
    pass


#Setting up tipracks and trash
solutions = containers.load('6-well-plate', '3', 'solutions')
trash = robot.fixed_trash
m300rack = containers.load('opentrons-tiprack-300ul', '4', 'm300-rack')
m50rack = containers.load('tiprack-Fisher200ul', '7', 'm50-rack')
m10rack = containers.load('tiprack-10ul', '1', 'm10-rack')


#Container Settings
if container_choice == "full_alumina":
    #Aluminum plate
    plate = labware.load('full_alumina', '2')

if container_choice == "half_alumina":
	#half aluminum plate
	plate = labware.load('half_alumina_plate', '2',)

if container_choice == "cups":
    #Cups plate
    plate_1 = labware.load('metal_cups_part1', '6')
    plate_2 = labware.load('metal_cups_part2', '6', share=True)
    plate_3 = labware.load('metal_cups_part3', '6', share=True)
    plate_4 = labware.load('metal_cups_part4', '6', share=True)


#Pipette Settings
large_min_volume = 0

#Left Mount
if current_pipettes[0] == 300:
    #P300:
    large_pipette = instruments.P300_Single(mount="left", dispense_flow_rate = P300_dispense_rate, tip_racks=[m300rack], trash_container = trash)
    large_min_volume = P300_min_volume

if current_pipettes[0] == 50:
    #P50:
    if current_pipettes[0] > current_pipettes[1]:
        large_pipette = instruments.P50_Single(mount="left", dispense_flow_rate = P50_dispense_rate, tip_racks=[m50rack], trash_container = trash)
        large_min_volume = P50_min_volume
    else:
        small_pipette = instruments.P50_Single(mount="left", dispense_flow_rate = P50_dispense_rate, tip_racks=[m50rack], trash_container = trash)

if current_pipettes[0] == 10:
    #P10:
    small_pipette = instruments.P10_Single(mount="left", dispense_flow_rate = P10_dispense_rate , tip_racks=[m10rack], trash_container = trash)

#Right Mount
if current_pipettes[1] == 300:
    #P300: 
    large_pipette = instruments.P300_Single(mount="right", dispense_flow_rate = P300_dispense_rate, tip_racks=[m300rack], trash_container = trash)
    large_min_volume = P300_min_volume

if current_pipettes[1] == 50:
    #P50:
    if current_pipettes[1] > current_pipettes[0]:
        large_pipette = instruments.P50_Single(mount="right", dispense_flow_rate = P50_dispense_rate, tip_racks=[m50rack], trash_container = trash)
        large_min_volume = P50_min_volume
    else:
        small_pipette = instruments.P50_Single(mount="right", dispense_flow_rate = P50_dispense_rate, tip_racks=[m50rack], trash_container = trash)

if current_pipettes[1] == 10:
    #P10:
    small_pipette = instruments.P10_Single(mount="right", dispense_flow_rate = P10_dispense_rate, tip_racks=[m10rack], trash_container = trash)


#Defining functions
def allot(pipette, volume, solution, well, small_condition): #Aspirate function. Needs inputs: pipette, volume, solution position, well, solution number
    pipette.aspirate(volume, solution)
    #For all ul in the volume
    for index in range(int(math.ceil(volume))):
        #Distribute
        pipette.dispense(1, well.top(6))
    pipette.delay(seconds=0.1)
    pipette.blow_out()

    #Is this volume below the small volume exception?
    if (volume <= small_condition):
        pipette.move_to(well.top(0.5))
        if(volume <= 3):
            pipette.move_to(well.top(0))

def nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_well, volume, large_min_volume, sol_pos, well_pos, small_condition):
    if small_volume == less_than_crit_well: #ie: distribute this this iteration
        if (volume < large_min_volume) and (volume != 0):
            allot(small_pipette, volume_step_well, sol_pos, well_pos, small_condition)
        elif(volume == 0):
            robot.comment("0ul. Nothing is done.")
        else:
            allot(large_pipette, volume, sol_pos, well_pos, small_condition)

def checkerboard_distribution(pipette, volume, container_choice, solutions, small_condition, pairity):
	behaviour = []
	if pairity == "even":
		behaviour.append('k*2')
		behaviour.append('k*2+1')
	if pairity == "odd":
		behaviour.append('k*2+1')
		behaviour.append('k*2')

	if container_choice == 'full_alumina':
	    for j in range(8):
	        for k in range(4):
	            #Is our column even or odd?
	            if (j%2) == 0:
	                #We are in an even column
	                allot(pipette, volume, solutions[position], plate.cols(j).wells(behaviour[0]), small_condition)
	            else:
	                #We are in an odd column
                    allot(pipette, volume, solutions[position], plate.cols(j).wells(behaviour[1]), small_condition)

	if container_choice == 'half_alumina':
	    for j in range(4):
	        for k in range(4):
	            #Is our column even or odd?
	            if (j%2) == 0:
	                #We are in an even column
	                allot(pipette, volume, solutions[position], plate.cols(j).wells(behaviour[0]), small_condition)
	            else:
	                #We are in an odd column
	                allot(pipette, volume, solutions[position], plate.cols(j).wells(behaviour[1]), small_condition)

	if container_choice == 'cups':
	    for j in range(2):
	        for k in range(4):
	            #Is our column even or odd?
	            if (j%2) == 0:
	                #We are in an even column
	                allot(pipette, volume, solutions[position], plate_1.cols(j).wells(behaviour[0]), small_condition)
	            else:
	                #We are in an odd column
	                allot(pipette, volume, solutions[position], plate_1.cols(j).wells(behaviour[1]), small_condition)

	    for j in range(2):
	        for k in range(4):
	            #Is our column even or odd?
	            if (j%2) == 0:
	                #We are in an even column
	                allot(pipette, volume, solutions[position], plate_2.cols(j).wells(behaviour[0]), small_condition)
	            else:
	                #We are in an odd column
	                allot(pipette, volume, solutions[position], plate_2.cols(j).wells(behaviour[1]), small_condition)

	    for j in range(2):
	        for k in range(4):
	            #Is our column even or odd?
	            if (j%2) == 0:
	                #We are in an even column
	                allot(pipette, volume, solutions[position], plate_3.cols(j).wells(behaviour[0]), small_condition)
	            else:
	                #We are in an odd column
	                allot(pipette, volume, solutions[position], plate_3.cols(j).wells(behaviour[1]), small_condition)

	    for j in range(2):
	        for k in range(4):
	            #Is our column even or odd?
	            if (j%2) == 0:
	                #We are in an even column
	                allot(pipette, volume, solutions[position], plate_4.cols(j).wells(behaviour[0]), small_condition)
	            else:
	                #We are in an odd column
	                allot(pipette, volume, solutions[position], plate.cols(j).wells(behaviour[1]), small_condition)
	pipette.drop_tip()

def solution_run_through(small_pipette, large_pipette, container_choice, small_volume, small_condition, solution_pos, list_of_solutions, solutions):
    for i in range(len(list_of_solutions)):
        #For each generic solution:
        position = solution_pos[i]

        #If we have a constant volume solution
        if len(list_of_solutions[i]) == 1:

            #1. What volume?
            volume = list_of_solutions[i][0]
            if volume < small_condition:
            	less_than_crit = True

            #2. Should we distribute this volume now? Yes, if this statement evaluates to True
            if small_volume == less_than_crit:

            	#3. Whats the right pipette?
            	if volume < large_min_volume:
            		small_pipette.pick_up_tip() 

            		#4. Ask the pipette to distribute the volume.
            		if container_choice == 'full_alumina':
            			for j in range(64):
            				allot(small_pipette, volume, solutions[position], plate.wells(j), small_condition)

            		if container_choice == 'half_alumina':
            			for j in range(32):
            				allot(small_pipette, volume, solutions[position], plate.wells(j), small_condition)

            		if container_choice == 'cups':
            			for j in range(16):
            				allot(small_pipette, volume, solutions[position], plate_1.wells(j), small_condition)
            			for j in range(16):
            				allot(small_pipette, volume, solutions[position], plate_2.wells(j), small_condition)
            			for j in range(16):
            				allot(small_pipette, volume, solutions[position], plate_3.wells(j), small_condition)
            			for j in range(16):
            				allot(small_pipette, volume, solutions[position], plate_4.wells(j), small_condition)

            		small_pipette.drop_tip()

	            else:
	                large_pipette.pick_up_tip()

	                #4. Ask the pipette to distribute the volume
	                if container_choice == 'full_alumina':
	                    for j in range(64):
	                        allot(large_pipette, volume, solutions[position], plate.wells(j), small_condition)

	                if container_choice == 'half_alumina':
	                    for j in range(32):
	                        allot(large_pipette, volume, solutions[position], plate.wells(j), small_condition)

	                if container_choice == 'cups':
	                    for j in range(16):
	                        allot(large_pipette, volume, solutions[position], plate_1.wells(j), small_condition)
	                    for j in range(16):
	                        allot(large_pipette, volume, solutions[position], plate_2.wells(j), small_condition)
	                    for j in range(16):
	                        allot(large_pipette, volume, solutions[position], plate_3.wells(j), small_condition)
	                    for j in range(16):
	                        allot(large_pipette, volume, solutions[position], plate_4.wells(j), small_condition)
	                large_pipette.drop_tip()
	                #Done with constant volume protocol


        #If we have a checkerboard distribution:
        if len(list_of_solutions[i]) == 2:

            #1. What volume?
            volume = list_of_solutions[i][0]
            if volume < small_condition:
                less_than_crit = True

            #2. Should we distribute this volume now? Yes, if this statement evaluates to True
            if small_volume == less_than_crit:

                #3. What pipette is best?
                if volume < large_min_volume:
                    small_pipette.pick_up_tip()

                    #3. Even or odd?
                    if list_of_solutions[i][1] == "even":
                        #4. Ask the pipette to distribute the volume
                        checkerboard_distribution(small_pipette, volume, container_choice, solutions, small_condition, 'even')

                    #3. Even or odd?
                    if list_of_solutions[i][1] == "odd":
                        #4. Ask the pipette to distribute the volume
                        checkerboard_distribution(small_pipette, volume, container_choice, solutions, small_condition, 'odd')

                else:
                    large_pipette.pick_up_tip()
                    #3. Even or odd?
                    if list_of_solutions[i][1] == "even":
                        #4. Ask the pipette to distribute the volume
                        checkerboard_distribution(large_pipette, volume, container_choice, solutions, small_condition, 'even')

                    #3. Even or odd?
                    if list_of_solutions[i][1] == "odd":
                        #4. Ask the pipette to distribute the volume
                        checkerboard_distribution(large_pipette, volume, container_choice, solutions, small_condition, 'odd')

                #Done with checkerboard protocol
	

        #If we have a 1D Gradient solution
        if len(list_of_solutions[i]) == 3:

            #1. What is the volume gradient?
            start = list_of_solutions[i][0]
            end = list_of_solutions[i][1]
            #Create a list of volume each well
            if start > end:
                step = (start-end)/7
                volume_steps = [start, start-step, start-(2*step), start-(3*step), start-(4*step), start-(5*step), start-(6*step), end]
            else:
                step = (end-start)/7
                volume_steps = [start, start+step, start+(2*step), start+(3*step), start+(4*step), start+(5*step), start+(6*step), end]
            
            #Initial check of range of distribution and creating a less_than_crit array.
            less_than_crit_array = []
            for index in range(volume_steps):
            	if volume_steps[index] < small_condition:
            		less_than_crit = True
            		less_than_crit_array.append(less_than_crit)
            	else:
            		less_than_crit_array.append(False)

            #2. What direction is the gradient?
            direction = list_of_solutions[i][2]

            #3. Which pipettes will be used? Only do this if some of this distribution will be done this iteration.
            if small_volume == less_than_crit:
	            if (start<large_min_volume) or (end<large_min_volume):
	                #The small pipette will be used at some point
	                small_pipette.pick_up_tip()

	            if (start>=large_min_volume) or (end>=large_min_volume):
	                #The large pipette will be used at some point
	                large_pipette.pick_up_tip()

            #4. Now we're ready to ask the robot to distribute this solution
            if direction == "x":
                #Gradient is along x -> across rows.

                if container_choice == 'full_alumina':
                    for j in range(8):
                        for k in range(8):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[k], volume_steps[k], large_min_volume, solutions[position], plate.rows(j).wells(k), small_condition)

                if container_choice == 'half_alumina':
                	#We need to write a different volume_steps for this container
                	if start > end:
                		step = (start-end)/3
                		volume_steps = [start, start-step, start-(2*step), end]
                	else:
                		step = (end-start)/3
                		volume_steps = [start, start+step, start+(2*step), end]

                	for j in range(8):
                		for k in range(4):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[k], volume_steps[k], large_min_volume, solutions[position], plate.rows(j).wells(k), small_condition)

                if container_choice == 'cups':
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[k], volume_steps[k], large_min_volume, solutions[position], plate_1.rows(j).wells(k), small_condition)

                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[k+2], volume_steps[k+2], large_min_volume, solutions[position], plate_2.rows(j).wells(k), small_condition)

                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[k+4], volume_steps[k+4], large_min_volume, solutions[position], plate_3.rows(j).wells(k), small_condition)

                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[k+6], volume_steps[k+6], large_min_volume, solutions[position], plate_4.rows(j).wells(k), small_condition)             

            if direction == "y":
                #Gradient is along y -> down columns.

                if container_choice == 'full_alumina':
                    for j in range(8):
                        for k in range(8):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[k], volume_steps[k], large_min_volume, solutions[position], plate.cols(j).wells(k), small_condition)

                if container_choice == 'half_alumina':
                	for j in range(4):
                		for k in range(8):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[k], volume_steps[k], large_min_volume, solutions[position], plate.cols(j).wells(k), small_condition)

                if container_choice == 'cups':
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[k], volume_steps[k], large_min_volume, solutions[position], plate_1.cols(j).wells(k), small_condition)

                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[k+2], volume_steps[k+2], large_min_volume, solutions[position], plate_2.cols(j).wells(k), small_condition)

                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[k+4], volume_steps[k+4], large_min_volume, solutions[position], plate_3.cols(j).wells(k), small_condition)

                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[k+6], volume_steps[k+6], large_min_volume, solutions[position], plate_4.cols(j).wells(k), small_condition)

            #5. Drop the used pipette tips
            if small_volume == less_than_crit: #Something was done for this solution during this iteration.
	            if (start<large_min_volume) or (end<large_min_volume):
	                #The small pipette was used at some point
	                small_pipette.drop_tip()

	            if (start>=large_min_volume) or (end>=large_min_volume):
	                #The large pipette was used at some point
	                large_pipette.drop_tip()

            #Done with 1D gradient protocol


        #If we have a 2D volume gradient:
        if len(list_of_solutions[i]) == 4:

            #1. What's the volume gradient
            start = list_of_solutions[i][0]
            end = list_of_solutions[i][1]
            #Create list of volume per well
            if start > end:
                step = (start-end)/14
                volume_steps = [start, start-step, start-(2*step), start-(3*step), start-(4*step), start-(5*step), start-(6*step), 
                				start-(7*step), start-(8*step), start-(9*step), start-(10*step), start-(11*step), start-(12*step),
                				start-(13*step), end]
            else :
                step = (end-start)/14
                volume_steps = [start, start+step, start+(2*step), start+(3*step), start+(4*step), start+(5*step), start+(6*step),
                				start+(7*step), start+(8*step), start+(9*step), start+(10*step), start+(11*step), start+(12*step),
                				start+(13*step), end]

            #Initial check of range of distribution and creating a less_than_crit array.
            less_than_crit_array = []
            for index in range(volume_steps):
            	if volume_steps[index] < small_condition:
            		less_than_crit = True
            		less_than_crit_array.append(less_than_crit)
            	else:
            		less_than_crit_array.append(False)

            #2. Which pipettes will be used?
            if small_volume == less_than_crit:
	            if (start<large_min_volume) or (end<large_min_volume):
	                #The small pipette will be used at some point
	                small_pipette.pick_up_tip()

	            if (start>=large_min_volume) or (end>=large_min_volume):
	                #The large pipette will be used at some point
	                large_pipette.pick_up_tip()

            #3. Now we're ready to ask the robot to distribute this solution
            if container_choice == 'full_alumina':
                for j in range(8):
                    for k in range(8):
                        nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j+k], volume_steps[j+k], large_min_volume, solutions[position], plate.rows(j).wells(k), small_condition)

            if container_choice == 'cups':
                for j in range(8):
                	for k in range(2):
                        nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j+k], volume_steps[j+k], large_min_volume, solutions[position], plate_1.rows(j).wells(k), small_condition)

                for j in range(8):
                    for k in range(2):
                        nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j+k+2], volume_steps[j+k+2], large_min_volume, solutions[position], plate_2.rows(j).wells(k), small_condition)

                for j in range(8):
                    for k in range(2):
                        nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j+k+4], volume_steps[j+k+4], large_min_volume, solutions[position], plate_3.rows(j).wells(k), small_condition)

                for j in range(8):
                    for k in range(2):
                        nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j+k+6], volume_steps[j+k+6], large_min_volume, solutions[position], plate_4.rows(j).wells(k), small_condition)
	            
            #4. Drop the used pipette tips
            if small_volume == less_than_crit: #If something was distributed for this solution this iteration.
	            if (start<large_min_volume) or (end<large_min_volume):
	                #The small pipette was used at some point
	                small_pipette.drop_tip()

	            if (start>=large_min_volume) or (end>=large_min_volume):
	                #The large pipette was used at some point
	                large_pipette.drop_tip()
            #Done with 2D gradient protocol


        #If we have a parallelogram distribution:
        if len(list_of_solutions[i]) == 5:

            #1. What's the volume gradient
            start = list_of_solutions[i][0]
            end = list_of_solutions[i][1]
            #Create list of volume per well
            for j in range(8):
                for k in range(8):
                    volume_steps[j][k] = start - (j*start/7) - ((start - (j*start/7))/7)*k

            #Initial check of range of distribution and creating a less_than_crit array
            for j in range(8):
                for k in range(8):
                    if volume_steps[j][k] < small_condition:
                        less_than_crit = True
                        less_than_crit_array[j][k] = less_than_crit
                    else:
                        less_than_crit_array[j][k] = False

            #2. What direction is the gradient?
            direction_array = []
            direction_array.append(list_of_solutions[i][2])
            direction_array.append(list_of_solutions[i][3])

            #3. Which pipettes will be used? Only do this if some of this distribution will be done this iteration.
            if small_volume == less_than_crit:
                if (start<large_min_volume) or (end<large_min_volume):
                    #The small pipette will be used at some point
                    small_pipette.pick_up_tip()

                if (start>=large_min_volume) or (end>=large_min_volume):
                    #The large pipette will be used at some point
                    large_pipette.pick_up_tip()

            #4. Now we're ready to ask the robot to distribute this solution
            if direction == [1,-1]:
                #Gradient is towards bottom right

                if container_choice == 'full_alumina':
                    for j in range(8):
                        for k in range(8):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j][k], volume_steps[j][k], large_min_volume, solutions[position], plate.rows(j).wells(k), small_condition)

                if container_choice == 'cups':
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j][k], volume_steps[j][k], large_min_volume, solutions[position], plate_1.rows(j).wells(k), small_condition)
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j][k+2], volume_steps[j][k+2], large_min_volume, solutions[position], plate_2.rows(j).wells(k), small_condition)
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j][k+4], volume_steps[j][k+4], large_min_volume, solutions[position], plate_3.rows(j).wells(k), small_condition)
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j][k+6], volume_steps[j][k+6], large_min_volume, solutions[position], plate_4.rows(j).wells(k), small_condition)             

            if direction == [1,1]:
                #Gradient is towards top right 

                if container_choice == 'full_alumina':
                    for j in range(8):
                        for k in range(8):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j][7-k], volume_steps[j][7-k], large_min_volume, solutions[position], plate.cols(j).wells(k), small_condition)

                if container_choice == 'cups':
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j][7-k], volume_steps[j][7-k], large_min_volume, solutions[position], plate_1.cols(j).wells(k), small_condition)
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j][7-k+2], volume_steps[j][7-k+2], large_min_volume, solutions[position], plate_2.cols(j).wells(k), small_condition)
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j][7-k+4], volume_steps[j][7-k+4], large_min_volume, solutions[position], plate_3.cols(j).wells(k), small_condition)
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[j][7-k+6], volume_steps[j][7-k+6], large_min_volume, solutions[position], plate_4.cols(j).wells(k), small_condition)

            if direction == [-1,1]:
                #Gradient is towards top left 

                if container_choice == 'full_alumina':
                    for j in range(8):
                        for k in range(8):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[7-j][7-k], volume_steps[7-j][7-k], large_min_volume, solutions[position], plate.cols(j).wells(k), small_condition)

                if container_choice == 'cups':
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[7-j][7-k], volume_steps[7-j][7-k], large_min_volume, solutions[position], plate_1.cols(j).wells(k), small_condition)
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[7-j][7-k+2], volume_steps[7-j][7-k+2], large_min_volume, solutions[position], plate_2.cols(j).wells(k), small_condition)
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[7-j][7-k+4], volume_steps[7-j][7-k+4], large_min_volume, solutions[position], plate_3.cols(j).wells(k), small_condition)
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[7-j][7-k+6], volume_steps[7-j][7-k+6], large_min_volume, solutions[position], plate_4.cols(j).wells(k), small_condition)

            if direction == [-1,-1]:
                #Gradient is towards bottom left

                if container_choice == 'full_alumina':
                    for j in range(8):
                        for k in range(8):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[7-j][k], volume_steps[7-j][k], large_min_volume, solutions[position], plate.cols(j).wells(k), small_condition)

                if container_choice == 'cups':
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[7-j][k], volume_steps[7-j][k], large_min_volume, solutions[position], plate_1.cols(j).wells(k), small_condition)
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[7-j][k+2], volume_steps[7-j][k+2], large_min_volume, solutions[position], plate_2.cols(j).wells(k), small_condition)
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[7-j][k+4], volume_steps[7-j][k+4], large_min_volume, solutions[position], plate_3.cols(j).wells(k), small_condition)
                    for j in range(8):
                        for k in range(2):
                            nonconstant_vol_procedure(small_pipette, large_pipette, small_volume, less_than_crit_array[7-j][k+6], volume_steps[7-j][k+6], large_min_volume, solutions[position], plate_4.cols(j).wells(k), small_condition)

            #5. Drop the used pipette tips
            if small_volume == less_than_crit: #Something was done for this solution during this iteration.
                if (start<large_min_volume) or (end<large_min_volume):
                    #The small pipette was used at some point
                    small_pipette.drop_tip()

                if (start>=large_min_volume) or (end>=large_min_volume):
                    #The large pipette was used at some point
                    large_pipette.drop_tip()

            #Done with parallelogram protocol


        #Done with this solution.


def protocol():
	less_than_crit = False
    list_of_solutions = []
    solution_pos =[]
    #Recording which solutions we are using.
    if len(solution_A) !=0 :
        list_of_solutions.append(solution_A)
        solution_pos.append('A1')
    if len(solution_B) !=0 :
        list_of_solutions.append(solution_B)
        solution_pos.append('B1')
    if len(solution_C) !=0 :
        list_of_solutions.append(solution_C)
        solution_pos.append('A2')
    if len(solution_D) !=0 :
        list_of_solutions.append(solution_D)
        solution_pos.append('B2')
    if len(precipitator) !=0 :
        list_of_solutions.append(precipitator)
        solution_pos.append('A3')

    #First run small volume solution_run_through
    small_volume = True
    solution_run_through(small_pipette, large_pipette, container_choice, small_volume, small_condition, solution_pos, list_of_solutions, solutions)

    #Then run large volume solution_run_through
    small_volume = False
    solution_run_through(small_pipette, large_pipette, container_choice, small_volume, small_condition, solution_pos, list_of_solutions, solutions)

    #End of entire protocol.

#Command
protocol(**{})