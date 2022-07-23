file = open("input.txt","r")
noofprocess = len(file.readlines()) - 1
file.seek(0)
process = []
arrivaltime = []
bursttime = []
i = 0
for line in file:
    if i==0:
        pass
    else:
        word = line.split()
        process.append(int(word[0]))
        arrivaltime.append(int(word[1]))
        bursttime.append(int (word[2]))
    i+=1
n = len(process)
wt = [0]*n
tat = [0]*n
rt = [0]*n
ct = [0]*n

# -------------------- FIRST COME FIRST SERVE-------------------------

def FCFS(n,bursttime,arrivaltime):
    wt = [0]*n
    tat = [0]*n
    rt = [0]*n
    ct = [0]*n

    print()
    print("----------------------------------------  FCFS  -----------------------------------------------------")
    # waiting time and response time (same in preemptive)
    for i in range(1,n):
        if ((arrivaltime[i - 1] + bursttime[i - 1] + wt[i - 1]) - arrivaltime[i]) < 0:
            wt[i] = 0
            rt[i] = 0
        else:
            wt[i] = (arrivaltime[i - 1] + bursttime[i - 1] + wt[i - 1]) - arrivaltime[i]
            rt[i] = (arrivaltime[i - 1] + bursttime[i - 1] + wt[i - 1]) - arrivaltime[i]
    # turn around time and completion time
    for i in range(n):
        tat[i] = wt[i] + bursttime[i]
        ct[i] = tat[i] + arrivaltime[i]

    print("\nProcess\t\tArrival Time\t\tBurst Time\t\tTurn Around Time\t\tWaiting Time\t\tResponse Time")
    for i in range(n):
        print("{}\t\t{:5d}\t\t{:12d}\t\t{:15d}\t\t{:22d}\t\t{:17d}".format(process[i],arrivaltime[i],bursttime[i],tat[i],wt[i],rt[i]))
    # gantt chart
    print("\nGantt Chart: ",end = "")
    for i in range(n):
        if i==0:
            for j in range(ct[i]):
                print(process[0],end="")
        else:
            for j in range(ct[i]-ct[i-1]):
                print(process[i],end="")

    # average turnaround time
    total = 0
    for i in range(n):
        total = total + tat[i]
    avg = total/n
    print("\nAVERAGE TURNAROUND TIME:",avg)
    # average waiting time
    total = 0
    for i in range(n):
        total = total + wt[i]
    avg = total/n
    print("AVERAGE WAITING TIME:",avg)
    # average response time
    total = 0
    for i in range(n):
        total = total + rt[i]
    avg = total/n
    print("AVERAGE RESPONSE TIME:",avg)
    # overall throughput
    print("OVERALL THROUGHPUT:",max(ct)/n)


# ------------------------------ SHORTEST JOB FIRST -----------------------------

def SJF(n,bursttime,arrivaltime):
    wt = [0]*n
    tat = [0]*n
    rt = [0]*n
    ct = [0]*n

    print()
    print("----------------------------------------  SJF  -----------------------------------------------------")
    # process
    table = []
    table.append(process);table.append(arrivaltime);table.append(bursttime);table.append(ct);table.append(wt);table.append(tat)
    # arrange arrival time
    for i in range(0, n):
        for j in range(i, n-i-1):
            if table[1][j] > table[1][j+1]:
                for k in range(0, n):
                    table[k][j], table[k][j+1] = table[k][j+1], table[k][j]
    # calculate completion time
    value = 0
    table[3][0] = table[1][0] + table[2][0] # calculating for first process
    table[5][0] = table[3][0] - table[1][0] # turnaround time
    table[4][0] = table[5][0] - table[2][0] # waiting time
    for i in range(1, n):
        temp = table[3][i-1]
        minimum = table[2][i]
        for j in range(i, n): # to find min burst time
            if temp >= table[1][j] and minimum >= table[2][j]:
                minimum = table[2][j]
                value = j
        table[3][value] = temp + table[2][value]
        table[5][value] = table[3][value] - table[1][value] # turnaround time
        table[4][value] = table[5][value] - table[2][value] # waiting time
        for k in range(0, 6):
            table[k][value], table[k][i] = table[k][i], table[k][value]
        for i in range(0, n):
            wt[i] = table[4][i]
            rt[i] = table[4][i] # wt = rt as non preemptive
            tat[i] = table[5][i]
    print("\nProcess\t\tArrival Time\t\tBurst Time\t\tTurn Around Time\t\tWaiting Time\t\tResponse Time")
    for i in range(n):
        print("{}\t\t{:5d}\t\t{:12d}\t\t{:15d}\t\t{:22d}\t\t{:17d}".format(process[i],arrivaltime[i],bursttime[i],tat[i],wt[i],rt[i]))

    print("\nGantt Chart: ",end = "")
    for i in range(n):
        if i==0:
            for j in range(ct[i]):
                print(process[0],end="")
        else:
            for j in range(ct[i]-ct[i-1]):
                print(process[i],end="")
    # average turnaround time
    total = 0
    for i in range(n):
        total = total + tat[i]
    avg = total/n
    print("\nAVERAGE TURNAROUND TIME:",avg)
    # average waiting time
    total = 0
    for i in range(n):
        total = total + wt[i]
    avg = total/n
    print("AVERAGE WAITING TIME:",avg)
    # average response time
    total = 0
    for i in range(n):
        total = total + rt[i]
    avg = total/n
    print("AVERAGE RESPONSE TIME:",avg)
    # overall throughput
    print("OVERALL THROUGHPUT:",max(ct)/n)

# -------------------- SHORTEST REMAINING TIME FIRST -------------------------

def SRTF(n,bursttime,arrivaltime):
    print()
    print("----------------------------------------  SRTF -----------------------------------------------------")
    queue = []
    for i in range(n):
        queue.append([])
        queue[i].append(process[i])
        queue[i].append(arrivaltime[i])
        queue[i].append(bursttime[i])
    wt=[0]*n
    rt=[0]*n
    tat=[0]*n
    remaining_time = [0]*n
    # waiting time
    for i in range(n):
        remaining_time[i] = queue[i][2]
    all_done = 0; value = 0 ; current_time=0
    minimum_time = 9999999999 ; flag = False
    response_time = 0 ; list = []
    print("\nGantt Chart: ",end="")
    while all_done!=n:
        for i in range(n):
            # Finding process with minimum remaining time and which is arrived till the current time
            if queue[i][1] <= current_time and remaining_time[i] < minimum_time and remaining_time[i]>0:
                minimum_time = remaining_time[i]
                value = i
                flag = True
        if flag==False: # if cpu is idle
            current_time = current_time + 1
            continue
        remaining_time[value] = remaining_time[value] - 1
        print(str(queue[value][0]),end="")
        # response time
        if queue[value][0] not in list:
            list.append(queue[value][0])
            response_time = response_time + current_time
            response_time = response_time - queue[value][1]
            rt[value] = response_time

        minimum_time = remaining_time[value]
        if minimum_time==0: # if mintime = 0 then we have to start again
            minimum_time = 9999999999
        if remaining_time[value]==0: # process's execution is completed
            all_done = all_done + 1
            flag = False
            finish_time = current_time + 1
            wt[value] = (finish_time - queue[value][1] - queue[value][2])# waiting time
            if wt[value]<0:
                wt[value] = 0
        current_time = current_time + 1
    print()
    for i in range(n):
        tat[i] = queue[i][2] + wt[i]
    print("\nProcess\t\tArrival Time\t\tBurst Time\t\tTurn Around Time\t\tWaiting Time\t\tResponse Time")
    for i in range(n):
        print("{}\t\t{:5d}\t\t{:12d}\t\t{:15d}\t\t{:22d}\t\t{:17d}".format(process[i],arrivaltime[i],bursttime[i],tat[i],wt[i],rt[i]))
    print("AVERAGE TURN AROUND TIME:",sum(tat)/n)
    print("AVERAGE WAITING TIME:",sum(wt)/n)
    print ("AVERAGE RESPONSE TIME:",(sum(rt)/n))
    print ("OVERALL THROUGHPUT:",(current_time/n))


# -------------------------- ROUND ROBIN ---------------------------------

def RR(no_of_processes,bursttime,arrivaltime):
    print("---------------------------------------  RR  ----------------------------------------------------")
    process_data = []
    for i in range(no_of_processes):
        temporary = []
        # '0' is the state of the process. 0 = not executed and 1 = execution complete
        temporary.extend([process[i], arrivaltime[i], bursttime[i], 0, bursttime[i]])
        process_data.append(temporary)
                
    # print(process_data) [[1, 0, 5, 0, 5], [2, 1, 4, 0, 4], [3, 2, 2, 0, 2], [4, 4, 1, 0, 1]]

    time_slice = int(input("Enter Time Slice: "))

    start_time = []
    exit_time = []
    executed_process = []
    ready_queue = []
    s_time = 0
    process_data.sort(key=lambda x: x[1]) # Sort processes according to the Arrival Time
    ganttchart = []
    while 1:
        normal_queue = []
        temp = []
        for i in range(len(process_data)):
            if process_data[i][1] <= s_time and process_data[i][3] == 0:
                present = 0
                if len(ready_queue) != 0: # checks that the next process is not a part of ready_queue
                    for k in range(len(ready_queue)):
                        if process_data[i][0] == ready_queue[k][0]:
                            present = 1

                if present == 0: #  adding a process to the ready_queue only if it is not already present in it
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    ready_queue.append(temp)
                    temp = []  
                    
                if len(ready_queue) != 0 and len(executed_process) != 0: # Adding the recently executed process to end of ready queue 
                    for k in range(len(ready_queue)):
                        if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                            ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))
                    
            elif process_data[i][3] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                normal_queue.append(temp)
                temp = []
        if len(ready_queue) == 0 and len(normal_queue) == 0:
            break
        if len(ready_queue) != 0:
            if ready_queue[0][2] > time_slice:
                    # remaining burst time greater than the time slice then execute for time = time slice
                start_time.append(s_time)
                s_time = s_time + time_slice
                ganttchart.append(str(ready_queue[0][0])*time_slice)
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(ready_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == ready_queue[0][0]:
                        break
                process_data[j][2] = process_data[j][2] - time_slice
                ready_queue.pop(0)
            elif ready_queue[0][2] <= time_slice:
                    # remaining burst time less than or equal the time slice then complete execution of process is done
                start_time.append(s_time)
                s_time = s_time + ready_queue[0][2]
                ganttchart.append(str(ready_queue[0][0])*ready_queue[0][2])
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(ready_queue[0][0])
                for j in range(len(process_data)):
                    if process_data[j][0] == ready_queue[0][0]:
                        break
                process_data[j][2] = 0
                process_data[j][3] = 1
                process_data[j].append(e_time)
                ready_queue.pop(0)
            elif len(ready_queue) == 0:
                if s_time < normal_queue[0][1]:
                    s_time = normal_queue[0][1]
                if normal_queue[0][2] > time_slice:
                    # remaining burst time greater than the time slice then execute for time = time slice
                    start_time.append(s_time)
                    s_time = s_time + time_slice
                    ganttchart.append(str(normal_queue[0][0])*time_slice)
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    process_data[j][2] = process_data[j][2] - time_slice
                elif normal_queue[0][2] <= time_slice:
                    # remaining burst time less than or equal the time slice then complete execution of process is done
                    start_time.append(s_time)
                    s_time = s_time + normal_queue[0][2]
                    ganttchart.append(str(normal_queue[0][0])*normal_queue[0][2])
                    e_time = s_time
                    exit_time.append(e_time)
                    executed_process.append(normal_queue[0][0])
                    for j in range(len(process_data)):
                        if process_data[j][0] == normal_queue[0][0]:
                            break
                    process_data[j][2] = 0
                    process_data[j][3] = 1
                    process_data[j].append(e_time)
    
    total_turnaround_time = 0 # turnaround_time = completion_time - arrival_time

    for i in range(len(process_data)):
        turnaround_time = process_data[i][5] - process_data[i][1]
        total_turnaround_time = total_turnaround_time + turnaround_time
        process_data[i].append(turnaround_time)
    t_time= total_turnaround_time / len(process_data)
    total_waiting_time = 0 #     waiting_time = turnaround_time - burst_time
    for i in range(len(process_data)):
        waiting_time = process_data[i][6] - process_data[i][4]
        total_waiting_time = total_waiting_time + waiting_time
        process_data[i].append(waiting_time)
    w_time = total_waiting_time / len(process_data)
    # print(start_time)
    # print(exit_time)
    print("Ganttchart:",ganttchart)
    print("\nProcess\t\tArrival Time\t\tBurst Time\t\tTurn Around Time\t\tWaiting Time\t\tCompletion time")
    for i in range(no_of_processes):
        print("{}\t\t{:5d}\t\t{:12d}\t\t{:15d}\t\t{:22d}\t\t{:17d}".format(process[i],arrivaltime[i],bursttime[i],(process_data[i][5] - process_data[i][1]),(process_data[i][6] - process_data[i][4]),(process_data[i][5] - process_data[i][1] + arrivaltime[i])))
    print('AVERAGE TURNAROUND TIME:',t_time)
    print('AVERAGE WAITING TIME:',w_time)
    print('OVERALL THROUGHPUT:',exit_time[no_of_processes-1]/no_of_processes)
    print('Sequence:',executed_process)

while True:
    print("---------------------------MENU----------------------------")
    print("1. FCFS")
    print("2. SJF")
    print("3. SRTF")
    print("4. RR")
    print("5. Exit")
    c = int(input("Enter choice: "))
    print()
    if c==1:
        FCFS(n,bursttime,arrivaltime) 
        print()
    elif c==2:
        SJF(n,bursttime,arrivaltime)
        print()
    elif c==3:
        SRTF(n,bursttime,arrivaltime)
        print()
    elif c==4:
        RR(n,bursttime,arrivaltime)
        print()
    elif c==5:
        exit()
    else:
        print("Enter valid choice!")