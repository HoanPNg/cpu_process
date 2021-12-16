class process:
    def __init__(self, name, arrival_time, cpu_burst, priority):
        self.name = name
        self.arrival_time = arrival_time
        self.cpu_burst = cpu_burst
        self.priority = priority
        
    @classmethod
    def from_string(cls, string):
        attribute = string.split(" ")
        return cls(attribute[0],attribute[1],attribute[2],attribute[3])

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
    for i in range(num_of_process):
        process_list.append(file_in.readline().rstrip("\n"))
    
    return num_of_process, quantum_time, process_list


num_of_pro, quantum_time, process_list = read_file()
print(num_of_pro)
print(quantum_time)
print(process_list)