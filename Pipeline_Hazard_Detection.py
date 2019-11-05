# Julia Thee
# CIS 655
# Final Project

""" HOW TO RUN PROGRAM """
""" To run this program, click the 'run' option in the top menu bar, followed by 'run module'. If you are using a version of Python other than
    Python 3.6.0, you may not have the exact same menu bar, so click whichever run/run module option your Python version has. Once you run this
    code, the shell will open, and the program will automatically ask you to input how many MIPS instructions you'd like to input; type an integer
    to indicate the number of instructions you will provide, then press enter. The program will then request you to input each MIPS instruction
    one by one; press enter after typing each one. The MIPS instruction should be four words/elements long, so put a space after the instruction
    name (e.g. 'add','lw','and', etc), as well as after each register. If you are typing an instruction that has an offset, such as a load or store
    instruction, that offset should be its own element, so put a space before and after it. Examples of input instructions: 'add $r1 $r2 $r3';
    'lw $r4 0 $r8'; 'beq $s0 $s1 loop'. Once the last instruction is entered, the program will produce its output. If you want to run this program
    while already in the shell, type 'pipeline()' into the shell.
"""



def pipeline():
    """ pipeline timing sequence used: IF ID EX ME WB """
    
    """"""""""""""""""""" GET INSTRUCTIONS """""""""""""""""""""""""""""

    """ get MIPS instructions from user """
    instrCount = int(input('How many instructions? '))  # request input from user
    instrList = []
    for i in range(instrCount):
        # request user to input each MIPS instruction one by one, making each instruction into a list of elements split up by white spaces
        # add each instruction (list of four elements) into 'instrList' array (so instrList is a list of lists)  
        instrList.append(list(map(str, input('Enter MIPS instruction ' + str(i+1) +': ').split())))
    print('\n')


    """"""""""""""""""""" DATA HAZARDS """""""""""""""""""""""""""""
    
    """ Detect data hazards; indicate data hazard in timing sequence with 'HZ';
        Read after write data hazards detected: instructions trying to read values from register before the data has been written to the register
    """
    # 'wbHazInstr' is list of instructions that could have data hazard due to conflict between ID and WB stages--list can be extended if desired
    # lw doesn't have data until 'ME' stage
    # the rest of the instructions in wbHazInstr have data in 'EX' stage
    wbHazInstr = ['add','sub','addi','addu','subu','and','or','slt','lw']   

    print("DATA HAZARDS\n")
    dHazArray = []  # array of timing sequence showing data hazards
    dHazCount = 0   # amount of data hazards detected
    indents = -1    # used to add spaces in dHazArray rows to show timing sequence per instruction
    stallArray = [[]]*instrCount   # keeps track of which instructions cause stalls/data hazards for later instructions
    for i in range(len(instrList)):
        dHazArray.append(['IF','ID','EX','ME','WB'])    # add list of timing sequence for each instruction into data hazard array
    
    for i in range(len(instrList)):
        if i<(len(instrList)-1):    # instruction is not the last one
            if instrList[i][0] in wbHazInstr:   # check for read after write hazard-- could this instruction cause ID/WB data hazard?
                if i<(len(instrList)-2):    # instruction is not the second to last one
                    # is instruction i+2 trying to read from register that instruction i needs to write to first?
                    if (instrList[i][1] == instrList[i+2][2]) or (instrList[i][1] == instrList[i+2][3]):
                        dHazCount += 1
                        dHazArray[i][4] = 'HZ'  # hazard in instruction i WB stage
                        dHazArray[i+2][1] = 'HZ'    # hazard in instruction i+2 ID stage
                        stallArray[i+2] = stallArray[i+2] + [i] # instruction i causing data hazard for instruction i+2
                        print("instruction "+str(i+3)+" needs "+str(instrList[i][1])+" value before instruction "+str(i+1)+" writes to it!")
                # is instruction i+1 trying to read from register that instruction i needs to write to first?
                if (instrList[i][1] == instrList[i+1][2]) or (instrList[i][1] == instrList[i+1][3]):
                    dHazCount += 1
                    dHazArray[i][4] = 'HZ'  
                    dHazArray[i+1][1] = 'HZ'    
                    stallArray[i+1] = stallArray[i+1] + [i] 
                    print("instruction "+str(i+2)+" needs "+str(instrList[i][1])+" value before instruction "+str(i+1)+" writes to it!")
                if instrList[i+1][0] == 'sw':
                # sw needs data for its first register by 'ME' stage
                    if (instrList[i][1] == instrList[i+1][1]):
                    # is 'sw' instruction trying to read from register that instruction i needs to write to first?
                        dHazCount += 1                  
                        dHazArray[i][4] = 'HZ'  
                        dHazArray[i+1][1] = 'HZ'
                        stallArray[i+1] = stallArray[i+1] + [i]
                        print("instruction "+str(i+2)+" needs "+str(instrList[i][1])+" value before instruction "+str(i+1)+" writes to it!")
    print('\n')
    for i in range(len(instrList)):
        # add spaces in dHazArray rows to show timing sequence-- one extra space each row
        indents += 1
        dHazArray[i] = ['  ']*indents + dHazArray[i]    
    print(str(dHazCount) + ' data hazard(s) found!')
    print("In the timing sequence below, 'HZ' indicates a hazard in the pipeline stage in which it appears:\n")
    makeStr(instrList, dHazArray)   # print out pipeline timing sequence
    print('\n')
    print("One option to fix the data hazard(s) is adding stalls, as shown below:")

    for i in range(len(stallArray)):
    # each element, i, in 'stallArray' contains a list of the instruction indexes that caused data hazard for instruction i
        for j in range(len(stallArray[i])): # iterate over all instructions that caused hazard for instruction i
            if 'HZ' in dHazArray[stallArray[i][j]]:
                hazIndex = dHazArray[stallArray[i][j]].index('HZ')  # get index of 'HZ' in row that caused hazard in WB stage
                hazIndex2 = dHazArray[i].index('HZ')    # get index of 'HZ' in row that caused hazard in ID stage
                diff = hazIndex - hazIndex2   # diff = how many columns apart are WB and ID hazards
                for k in range(diff):   # iterate over the amount of columns separating the hazards
                    addStall = i    # stalls will be added starting from instruction i
                    while addStall<len(instrList) : # add stall to every row from instruction i to the last instruction 
                        temp = 0
                        dHazArray[addStall] = ['  '] + dHazArray[addStall]  # add one whitespace to row that will have stall added
                        while dHazArray[addStall][temp] == '  ':    # iterate over whitespaces in the row
                            temp += 1
                        dHazArray[addStall][temp-1] = 'ST'  # add stall at beginning of timing sequence in row (in rightmost whitespace)
                        addStall += 1   # go to next row
                hazIndex = dHazArray[stallArray[i][j]].index('HZ')  
                hazIndex2 = dHazArray[i].index('HZ')
                dHazArray[stallArray[i][j]][hazIndex] = 'WB'  # change 'HZ' to 'WB' in row that caused hazard in WB stage
                dHazArray[i][hazIndex2] = 'ID'  # change 'HZ' to 'ID' in row that caused hazard in ID stage
    for i in range(len(dHazArray)):
    # after all stalls have been added, change any remaining 'HZ' in dHazArray to 'ID' 
        if 'HZ' in dHazArray[i]:
            dHazArray[i][dHazArray[i].index('HZ')] = 'ID'
    makeStr(instrList, dHazArray)   # print out pipeline timing sequence

    print("\nAdding stalls to solve the issue of data hazards can add a lot of clock cycles.")
    print("A better idea would be to use the forwarding technique to eliminate data hazards.")
    print("If forwarding doesn't fix all of the hazards, we'll need to add stalls:\n")

    """ Use forwarding technique to fix the data hazards;
        If forwarding can't solve a data hazard, such as from 'load' instruction not having data available for its first register
        until the 'ME' stage, then a stall will need to be added
    """

    dArray = []     # array of timing sequence showing data hazards fixed by forwarding
    indents = -1
    dHazStalls = [0]*instrCount   # array holding how many data hazards per instruction can't be fixed by forwarding (so needs to stall)
    for i in range(len(instrList)):
        dArray.append(['IF','ID','EX','ME','WB'])
    
    for i in range(len(instrList)):
        if i<(len(instrList)-1):    # instruction is not the last one
            if instrList[i][0] in wbHazInstr:   # check for read after write hazard
                if i<(len(instrList)-2):    # instruction is not the second to last one
                    if (instrList[i][1] == instrList[i+2][2]) or (instrList[i][1] == instrList[i+2][3]):
                        # forward from instruction i to instruction i+2
                        print("instruction "+str(i+1)+" forwards "+str(instrList[i][1])+" value from ME/WB register to ALU input latch, so "
                              "instruction "+str(i+3)+" does not need to stall!")
                        
                if (instrList[i][1] == instrList[i+1][2]) or (instrList[i][1] == instrList[i+1][3]):
                    # data hazard between instruction i and i+1
                    if (instrList[i][0] == 'lw') and (instrList[i+1][0] in wbHazInstr):
                        # lw doesn't have its data until 'ME' stage, but instruction i+1 needs it by 'EX' stage--need to stall
                        print("instruction "+str(i+2)+" needs "+str(instrList[i][1])+" value by 'EX' stage, but instruction "+str(i+1)+" does"
                              " not have the value until 'ME' stage! One stall cycle must be added.")
                        addStall = i+1   # add stall for in row starting from instruction i+1
                        while addStall<len(instrList):
                            dHazStalls[addStall] += 1
                            temp = 0
                            dArray[addStall] = ['  '] + dArray[addStall]
                            while dArray[addStall][temp] == '  ':
                                temp += 1
                            dArray[addStall][temp-1] = 'ST'
                            addStall += 1
                    else:
                        # forward from instruction i to instruction i+1
                        print("instruction "+str(i+1)+" forwards "+str(instrList[i][1])+" value from EX/ME register to ALU input latch, so "
                              "instruction "+str(i+2)+" does not need to stall!")
                    
                if instrList[i+1][0] == 'sw':
                    # 'sw' instruction doesn't need first register data until 'ME' stage
                    if (instrList[i][1] == instrList[i+1][1]):  
                        print("instruction "+str(i+1)+" forwards "+str(instrList[i][1])+" value from ME/WB register to memory input, so "
                              "instruction "+str(i+2)+" does not need to stall!")
    print('\n')
    for i in range(len(instrList)):
        # add spaces in dArray rows to show timing sequence-- one extra space each row
        indents += 1
        dArray[i] = ['  ']*indents + dArray[i]
    print("The new pipeline timing sequence after the forwarding technique was applied:\n")
    makeStr(instrList, dArray) # print out pipeline timing sequence
    print('\n')


    """"""""""""""""""""" STRUCTURAL HAZARDS """""""""""""""""""""""""""""
    
    """ Detect structural hazards; indicate structural hazard in timing sequence with 'HZ';
        Structural hazards result from combined instruction and data memory-- this memory is
        always used during 'IF' stage in pipeline, and used during 'ME' stage in loads and stores
    """

    print("\nSTRUCTURAL HAZARDS\n")
    
    sHazArray = []  # array of timing sequence showing structural hazards
    sHazCount = 0   # amount of structural hazards detected
    indents = -1    # used to add spaces in sHazArray rows to show timing sequence per instruction
    for i in range(len(instrList)):
        sHazArray.append(['IF','ID','EX','ME','WB']) # add list of timing sequence for each instruction into structural hazard array
        if (i>=3 and (instrList[i-3][0]=='lw' or instrList[i-3][0]=='sw')):
        # structural hazard caused if load/store trying to access data memory ('ME' stage) at the same time as 
        # another instruction is trying to access instruction memory ('IF' stage)
            sHazCount += 1
            sHazArray[i][0] = 'HZ'   # hazard in instruction i IF stage
            sHazArray[i-3][3] = 'HZ' # hazard in instruction i ME stage
            print("instruction "+str(i+1)+" and instruction "+str(i-2)+" are trying to access the combined I/D memory at the same time!")
    for i in range(len(instrList)):
        # add spaces in sHazArray rows to show timing sequence-- one extra space each row
        indents += 1
        sHazArray[i] = ['  ']*indents + sHazArray[i]
        
    print('\n')
    print(str(sHazCount) + ' structural hazard(s) found!')
    print("In the timing sequence below, 'HZ' indicates a hazard in the pipeline stage in which it appears:\n")

    makeStr(instrList, sHazArray)   # print out pipeline timing sequence
    print('\n')

    
    """ Add stalls in the pipeline timing sequence to fix the structural hazards;
        Stalls are represented as 'ST' in the timing sequence
    """
    
    print('Fix the structural hazards by adding stalls!\n')
    sHazArray2 = []   # array of timing sequence showing structural hazards fixed by adding stalls
    stalls = 0
    for i in range(len(instrList)):
        # stalls variable adds whitespaces to each row, one extra space per row
        sHazArray2.append(['  ']*stalls + ['IF','ID','EX','ME','WB'])
        stalls += 1
    sHazStalls = [0]*instrCount   # array needed for 'structHaz()' function to indicate no extra stalls currently exist for each instruction
    finalArray = structHaz(instrList,sHazArray2,sHazStalls)
    # structHaz() adds stalls to each row (as required) to fix structural hazards-- it returns the updated array


    """"""""""""""""""""" CONTROL HAZARDS """""""""""""""""""""""""""""
    
    """ Detect control hazards; indicate control hazard in timing sequence with 'HZ';
        Handle branches by flushing the pipeline (stall one cycle)
    """

    print("\nCONTROL HAZARDS\n")

    cHazArray = []  # array of timing sequence showing control hazards
    cHazCount = 0   # amount of control hazards detected
    indents = -1    # used to add spaces in cHazArray rows to show timing sequence per instruction
    for i in range(len(instrList)):
        cHazArray.append(['IF','ID','EX','ME','WB'])  # add list of timing sequence for each instruction into control hazard array
        if instrList[i][0]=='beq':
        # check if instruction is a branch--only checks for 'beq' but more branch instructions can be added if desired
            cHazCount += 1
            cHazArray[i][0] = 'HZ'  # hazard in instruction i IF stage (stall needs to be added)
            print("Branch detected: instruction "+str(i+1))
    for i in range(len(instrList)):
        # add spaces in sHazArray rows to show timing sequence-- one extra space each row
        indents += 1
        cHazArray[i] = ['  ']*indents + cHazArray[i]
    print('\n')
    print(str(cHazCount) + ' control hazard(s) found!')
    print("In the timing sequence below, 'HZ' indicates a hazard in the pipeline stage in which it appears:\n")
    makeStr(instrList, cHazArray)   # print out pipeline timing sequence
    print('\n')

    cHazArray2 = []   # array of timing sequence showing control hazards fixed by adding stall
    indents = -1
    for i in range(len(instrList)):
        cHazArray2.append(['IF','ID','EX','ME','WB'])
        if instrList[i][0]=='beq':
            addStall = i  # add stall to each row, starting at row i (the branch instruction)
            while addStall<len(instrList):
                temp = 0
                cHazArray2[addStall] = ['  '] + cHazArray2[addStall]
                while cHazArray2[addStall][temp] == '  ':
                    temp += 1
                cHazArray2[addStall][temp-1] = 'ST'
                addStall += 1
    for i in range(len(instrList)):
        # add spaces in sHazArray rows to show timing sequence-- one extra space each row
        indents += 1
        cHazArray2[i] = ['  ']*indents + cHazArray2[i]
        
    print("To fix the control hazard(s), flush the pipeline for each branch instruction detected (stall one cycle for each branch)\n")
    makeStr(instrList, cHazArray2) # print out pipeline timing sequence
    print('\n')


    print("Here is the timing sequence combining the data, structural, and control hazard solutions:\n")
    structHazWithBranch(instrList,finalArray,dHazStalls)
    # structHazWithBranch() adds stall for each branch instruction and each row following that instruction


""""""""""""""""""""" ADDITIONAL FUNCTIONS """""""""""""""""""""""""""""

def structHaz(instrList,sHazArray2,stallArr):
    """takes as input the original list of instructions, an array of a pipeline timing sequence for the instructions,
       and an array indicating the amount of stalls currently present in the timing sequence (stalls per instruction)
    """
    for i in range(len(instrList)):
        meIndex = 0         # which column has 'ME' causing hazard
        ifIndex = -1        # which row has 'IF' causing hazard 
        if instrList[i][0] == 'lw' or instrList[i][0] == 'sw':
        # only loads and stores cause structural hazard in the 'ME' stage
            for j in range(len(sHazArray2[i])):
                if sHazArray2[i][j] == 'ME':
                    meIndex = j  # 'ME' structural hazard located at column index j
            k = i+1  # local variable to keep track of row being checked for 'IF' structural hazard, starting at i+1 
            while k<len(instrList) and ifIndex == -1:
                # if this while loop quits, either no row has an 'IF' hazard or ifIndex has been set to row index with 'IF' hazard
                if sHazArray2[k][meIndex] == 'IF':
                    ifIndex = k  # 'IF' structural hazard located at row index k
                k += 1
            if ifIndex == -1:   # don't add stall(s) if no 'IF' hazard detected
                break
            addStall = ifIndex  # add stall(s) to each row, starting at ifIndex row
            while addStall<len(instrList):
                temp = 0
                sHazArray2[addStall] = ['  '] + sHazArray2[addStall]   # add one whitespace to row that will have stall added
                while sHazArray2[addStall][temp] == '  ':   # iterate over whitespaces in the row
                    temp += 1
                if stallArr[addStall] == 0:
                    sHazArray2[addStall][temp-1] = 'ST'     # replace rightmost whitespace with 'ST' to add stall
                else:
                    stallArr[addStall] = (stallArr[addStall] - 1)
                    # at least one stall was already in stallArr, so don't add another stall, but decrement stallArr
                addStall += 1

    makeStr(instrList, sHazArray2)  # print out pipeline timing sequence
    print('\n')
    return sHazArray2


def structHazWithBranch(instrList,sHazArray2,stallArr):
    """ takes as input the original list of instructions, an array of a pipeline timing sequence for the instructions,
        and an array indicating the amount of stalls currently present in the timing sequence (stalls per instruction)
        function adds one stall for each branch instruction i, and for every instruction following i
    """
    for i in range(len(instrList)):
        if instrList[i][0]=='beq':  # checks if instruction is a branch instruction
            addStall = i   # add stall to each row, starting at branch instruction i
            while addStall<len(instrList):
                temp = 0
                sHazArray2[addStall] = ['  '] + sHazArray2[addStall] 
                while sHazArray2[addStall][temp] == '  ':
                    temp += 1
                sHazArray2[addStall][temp-1] = 'ST'
                addStall += 1
                
    makeStr(instrList, sHazArray2)  # print out pipeline timing sequence
    print('\n')


def makeStr(instrList, array):
    """ Given the initial MIPS instructions array and a timing sequence array,
        convert the timing sequence into a string format
    """
    for i in range(len(instrList)):  # iterate over each instruction in input array
        instr = ''
        for j in range(len(array[i])):
            instr += array[i][j] + ' '
        if len(instrList[i][0]) == 3:
            print(str(i+1)+ '. '+' ' + str(instrList[i][0]) + ': ' + str(instr))
        elif len(instrList[i][0]) == 2:
            print(str(i+1)+ '. '+'  ' + str(instrList[i][0]) + ': ' + str(instr))
        else:
            print(str(i+1)+ '. '+str(instrList[i][0]) + ': ' + str(instr))
            


pipeline()
    



