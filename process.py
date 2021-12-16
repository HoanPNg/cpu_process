class process:
    def __init__(self, name, arrival_time, cpu_burst, priority):
        self.name = name
        self.arrival_time = arrival_time
        self.cpu_burst = cpu_burst
        self.priority = priority
        
    @classmethod
    def from_string(cls, string):
        attribute = string.split(" ")
        return cls(attribute[0],int(attribute[1]),int(attribute[2]),int(attribute[3]))

def get_cpu_burst(process):
    return process.cpu_burst

def get_remain_time(process):
    return process[1]

def get_priority(process):
    return process[0].priority

def read_file(filename):
    '''
        return number_of_prcesses, quantum_time, list_of_processes
    '''
    file_in = open(filename, "r")
    num_of_process = int(file_in.read(1))
    file_in.seek(2)
    quantum_time = int(file_in.read(1))

    file_in.seek(5)
    
    process_list = []
    process_list_string = []
    for i in range(num_of_process):
        process_list_string.append(file_in.readline().rstrip("\n"))
    
    for i in process_list_string:
        process_list.append(process.from_string(i))
    return num_of_process, quantum_time, process_list

#==============================FCDS=======================================
def FCFS(process_list: list[process]):
    num_of_process = len(process_list)
    finish_process = []
    scheduling_chart = ""
    process_queue = []
    time = 0
    total_TT = 0
    total_WT = 0
    last_in = process_list[0].arrival_time
    first_in = process_list[0].arrival_time
    for i in process_list:
        if last_in <= i.arrival_time:
            last_in = i.arrival_time
        
        if first_in >= i.arrival_time:
            first_in = i.arrival_time

    if first_in != 0:
        scheduling_chart += "0 ~x~ "
        scheduling_chart += (str(first_in)+ " ")
        time = first_in
    else:
        scheduling_chart += "0 "

    for i in range(last_in+1):
        for process in process_list:
            if i == process.arrival_time:
                process_queue.append(process)
    
    while(len(process_queue) != 0):
        running_process = process_queue.pop(0)
        scheduling_chart = scheduling_chart + "~" + running_process.name + "~ "
        time += running_process.cpu_burst
        scheduling_chart = scheduling_chart + str(time) + " "
        finish_process.append((running_process, time))
    
    scheduling_chart += "\n"
    file_out = open("FCFS.txt", "w")
    file_out.write("Scheduling chart: \n")
    file_out.write(scheduling_chart)
    for process in finish_process:
        file_out.write(process[0].name + ": ")
        file_out.write("TT =" + str(process[1] - process[0].arrival_time) +  " ")
        total_TT += process[1] - process[0].arrival_time
        file_out.write("WT =" + str(process[1] - process[0].arrival_time - process[0].cpu_burst) +  "\n")
        total_WT += process[1] - process[0].arrival_time - process[0].cpu_burst

    file_out.write("Average: TT = " + str(round((total_TT / num_of_process),2)) + " WT = " + str(round((total_WT / num_of_process),2)))


    file_out.close()
    
#==============================RR=======================================
def RR(process_list: list[process], quantum_time):
    num_of_process = len(process_list)
    added_process = []
    finish_process = []
    scheduling_chart = ""
    time = 0
    process_queue = []
    first_in = time
    total_TT = 0
    total_WT = 0


    while(len(process_queue) == 0):
        for i in process_list:
            if first_in == i.arrival_time:
                process_queue.append([i, i.cpu_burst])
                added_process.append(i)
        if len(process_queue) == 0:
            first_in +=1

    if first_in != 0:
        scheduling_chart += "0 ~x~ "
        scheduling_chart += (str(first_in) + " ")
        time = first_in
    else:
        scheduling_chart += "0 "

    while(len(process_queue) != 0):
        if len(process_list) != len(added_process):
            for temp_time in range(time, time+ quantum_time + 1):
                for i in process_list:
                    if (i.arrival_time == temp_time) and (i not in added_process):
                        added_process.append(i)
                        process_queue.append([i, i.cpu_burst])

        running_process = process_queue.pop(0)
        running_process_remain = running_process[1] - quantum_time
        

        if running_process_remain > 0:
            time += quantum_time
            scheduling_chart = scheduling_chart + "~" + running_process[0].name + "~ "
            scheduling_chart = scheduling_chart + str(time) + " "
            running_process[1] -= quantum_time
            process_queue.append(running_process)
        elif running_process_remain == 0:
            time += quantum_time
            scheduling_chart = scheduling_chart + "~" + running_process[0].name + "~ "
            scheduling_chart = scheduling_chart + str(time) + " "
            finish_process.append((running_process[0],time))
        else:
            time += running_process[1]
            scheduling_chart = scheduling_chart + "~" + running_process[0].name + "~ "
            scheduling_chart = scheduling_chart + str(time) + " "
            finish_process.append((running_process[0],time))
    
    scheduling_chart += "\n"
    finish_process.reverse()
    file_out = open("RR.txt", "w")
    file_out.write("Scheduling chart: \n")
    file_out.write(scheduling_chart)
    for process in finish_process:
        file_out.write(process[0].name + ": ")
        file_out.write("TT =" + str(process[1] - process[0].arrival_time) +  " ")
        total_TT += process[1] - process[0].arrival_time
        file_out.write("WT =" + str(process[1] - process[0].arrival_time - process[0].cpu_burst) +  "\n")
        total_WT += process[1] - process[0].arrival_time - process[0].cpu_burst

    file_out.write("Average: TT = " + str(round((total_TT / num_of_process),2)) + " WT = " + str(round((total_WT / num_of_process),2)))


    file_out.close()         

#==============================SRTN=======================================
def SRTN(process_list: list[process]):
    num_of_process = len(process_list)
    added_process = []
    finish_process = []
    scheduling_chart = ""
    time = 0
    process_queue = []
    first_in = time
    total_TT = 0
    total_WT = 0
    new_process = False

    while(len(process_queue) == 0):
        for i in process_list:
            if first_in == i.arrival_time:
                process_queue.append([i, i.cpu_burst])
                added_process.append(i)
        if len(process_queue) == 0:
            first_in +=1

    if first_in != 0:
        scheduling_chart += "0 ~x~ "
        scheduling_chart += (str(first_in) + " ")
        time = first_in
    else:
        scheduling_chart += "0 "

    while(len(process_queue) != 0):
        process_queue.sort(key=get_remain_time)
        running_process = process_queue.pop(0)

        if len(process_list) != len(added_process):
            for temp_time in range(time, time+ running_process[1] + 1):
                if new_process == True:
                    time = temp_time -1
                    break
                for i in process_list:
                    if (i.arrival_time == temp_time) and (i not in added_process):
                        added_process.append(i)
                        process_queue.append([i, i.cpu_burst])
                        new_process = True
                        process_queue.append([running_process[0],running_process[1] - (temp_time - time) ])
                    if new_process == True:
                        break
                
        if new_process == True:
            new_process = False
            scheduling_chart = scheduling_chart + "~" + running_process[0].name + "~ "
            scheduling_chart = scheduling_chart + str(time) + " "
        else:
            scheduling_chart = scheduling_chart + "~" + running_process[0].name + "~ "
            time += running_process[1]
            scheduling_chart = scheduling_chart + str(time) + " "
            finish_process.append((running_process[0], time))
    
    scheduling_chart += "\n"
    finish_process.reverse()

    file_out = open("SRTN.txt", "w")
    file_out.write("Scheduling chart: \n")
    file_out.write(scheduling_chart)
    for process in finish_process:
        file_out.write(process[0].name + ": ")
        file_out.write("TT =" + str(process[1] - process[0].arrival_time) +  " ")
        total_TT += process[1] - process[0].arrival_time
        file_out.write("WT =" + str(process[1] - process[0].arrival_time - process[0].cpu_burst) +  "\n")
        total_WT += process[1] - process[0].arrival_time - process[0].cpu_burst

    file_out.write("Average: TT = " + str(round((total_TT / num_of_process),2)) + " WT = " + str(round((total_WT / num_of_process),2)))
    file_out.close()
    

#==============================Priority=======================================
def Priority(process_list: list[process]):
    num_of_process = len(process_list)
    added_process = []
    finish_process = []
    scheduling_chart = ""
    time = 0
    process_queue = []
    first_in = time
    total_TT = 0
    total_WT = 0
    new_process = False

    while(len(process_queue) == 0):
        for i in process_list:
            if first_in == i.arrival_time:
                process_queue.append([i, i.cpu_burst])
                added_process.append(i)
        if len(process_queue) == 0:
            first_in +=1

    if first_in != 0:
        scheduling_chart += "0 ~x~ "
        scheduling_chart += (str(first_in) + " ")
        time = first_in
    else:
        scheduling_chart += "0 "

    while(len(process_queue) != 0):
        process_queue.sort(key=get_priority)
        running_process = process_queue.pop(0)

        if len(process_list) != len(added_process):
            for temp_time in range(time, time+ running_process[1] + 1):
                if new_process == True:
                    time = temp_time -1
                    break
                for i in process_list:
                    if (i.arrival_time == temp_time) and (i not in added_process):
                        added_process.append(i)
                        process_queue.append([i, i.cpu_burst])
                        new_process = True
                        process_queue.append([running_process[0],running_process[1] - (temp_time - time) ])
                    if new_process == True:
                        break
                
        if new_process == True:
            new_process = False
            scheduling_chart = scheduling_chart + "~" + running_process[0].name + "~ "
            scheduling_chart = scheduling_chart + str(time) + " "
        else:
            scheduling_chart = scheduling_chart + "~" + running_process[0].name + "~ "
            time += running_process[1]
            scheduling_chart = scheduling_chart + str(time) + " "
            finish_process.append((running_process[0], time))
    
    scheduling_chart += "\n"
    finish_process.reverse()

    file_out = open("Priority.txt", "w")
    file_out.write("Scheduling chart: \n")
    file_out.write(scheduling_chart)
    for process in finish_process:
        file_out.write(process[0].name + ": ")
        file_out.write("TT =" + str(process[1] - process[0].arrival_time) +  " ")
        total_TT += process[1] - process[0].arrival_time
        file_out.write("WT =" + str(process[1] - process[0].arrival_time - process[0].cpu_burst) +  "\n")
        total_WT += process[1] - process[0].arrival_time - process[0].cpu_burst

    file_out.write("Average: TT = " + str(round((total_TT / num_of_process),2)) + " WT = " + str(round((total_WT / num_of_process),2)))
    file_out.close()

#==============================SRTN=======================================
def SJF(process_list: list[process]):
    num_of_process = len(process_list)
    added_process = []
    finish_process = []
    scheduling_chart = ""
    time = 0
    process_queue = []
    first_in = time
    total_TT = 0
    total_WT = 0

    while(len(process_queue) == 0):
        for i in process_list:
            if first_in == i.arrival_time:
                process_queue.append(i)
                added_process.append(i)
        if len(process_queue) == 0:
            first_in +=1

    if first_in != 0:
        scheduling_chart += "0 ~x~ "
        scheduling_chart += (str(first_in) + " ")
        time = first_in
    else:
        scheduling_chart += "0 "

    while(len(process_queue) != 0):
        process_queue.sort(key=get_cpu_burst)
        running_process = process_queue.pop(0)

        if len(process_list) != len(added_process):
            for temp_time in range(time, time + running_process.cpu_burst + 1):
                for i in process_list:
                    if (i.arrival_time == temp_time) and (i not in added_process):
                        added_process.append(i)
                        process_queue.append(i)
                
        scheduling_chart = scheduling_chart + "~" + running_process.name + "~ "
        time += running_process.cpu_burst
        scheduling_chart = scheduling_chart + str(time) + " "
        finish_process.append((running_process, time))
    
    scheduling_chart += "\n"
    finish_process.reverse()

    file_out = open("SJF.txt", "w")
    file_out.write("Scheduling chart: \n")
    file_out.write(scheduling_chart)
    for process in finish_process:
        file_out.write(process[0].name + ": ")
        file_out.write("TT =" + str(process[1] - process[0].arrival_time) +  " ")
        total_TT += process[1] - process[0].arrival_time
        file_out.write("WT =" + str(process[1] - process[0].arrival_time - process[0].cpu_burst) +  "\n")
        total_WT += process[1] - process[0].arrival_time - process[0].cpu_burst

    file_out.write("Average: TT = " + str(round((total_TT / num_of_process),2)) + " WT = " + str(round((total_WT / num_of_process),2)))
    file_out.close()


#======Main========
num_of_process, quantum_time, process_list = read_file("input.txt")
FCFS(process_list)
RR(process_list,quantum_time)
SRTN(process_list)
Priority(process_list)
SJF(process_list)