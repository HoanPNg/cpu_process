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

def read_file():
    '''
        return number_of_prcesses, quantum_time, list_of_processes
    '''
    file_in = open("input.txt", "r")
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

def FCFS(process_list: list[process]):
    num_of_process = len(process_list)
    finish_process = []
    scheduling_chart = ""
    process_queue = []
    file_out = open("FCFS.txt", "w")
    file_out.write("Scheduling chart: \n")
    time = 0
    max_time = 0
    last_in = process_list[0].arrival_time
    first_in = process_list[0].arrival_time
    for i in process_list:
        max_time += i.cpu_burst
        if last_in <= i.arrival_time:
            last_in = i.arrival_time
        
        if first_in >= i.arrival_time:
            first_in = i.arrival_time

    if first_in != 0:
        scheduling_chart += "0 ~x~ "
        scheduling_chart += str(first_in)
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
    file_out.write(scheduling_chart)
    total_TT = 0
    total_WT = 0
    for process in finish_process:
        file_out.write(process[0].name + ": ")
        file_out.write("TT =" + str(process[1] - process[0].arrival_time) +  " ")
        total_TT += process[1] - process[0].arrival_time
        file_out.write("WT =" + str(process[1] - process[0].cpu_burst) +  "\n")
        total_WT += process[1] - process[0].cpu_burst

    file_out.write("Average: TT = " + str(round((total_TT / num_of_process),2)) + " WT = " + str(round((total_WT / num_of_process),2)))


    file_out.close()
    

num_of_pro, quantum_time, process_list = read_file()
print(num_of_pro)
print(quantum_time)
print(process_list)
FCFS(process_list)