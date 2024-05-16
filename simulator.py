from collections import deque
import sys

class Process:
    def __init__(self, number, arrival_time, burst_time):
        self.number = number
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = 0
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.state = 'r'  # r: running, p: pending, f: finished, c: continued

class Scheduler:
    def __init__(self, processes):
        self.processes = processes
        self.schedule_queue = deque()
    def fcfs(self):
        self.processes.sort(key=lambda x: x.arrival_time)
        current_time = 0
        for p in self.processes:
            p.start_time = max(p.arrival_time, current_time)
            p.finish_time = p.start_time + p.burst_time
            p.turnaround_time = p.finish_time - p.arrival_time
            p.waiting_time = p.start_time - p.arrival_time
            current_time = p.finish_time
            p.state = 'f'
            self.schedule_queue.append(p)
        self.display_results("FCFS")


    def srt(self):
        self.processes.sort(key=lambda x: x.arrival_time)
        current_time = 0
        completed_processes = 0
        while completed_processes < len(self.processes):
            # Find process with the smallest remaining time that has arrived
            eligible_processes = [p for p in self.processes if p.arrival_time <= current_time and p.state != 'f']
            if not eligible_processes:
                current_time += 1
                continue
            current_process = min(eligible_processes, key=lambda x: x.remaining_time)
            
            # Process execution
            if current_process.state == 'r':
                current_process.state = 'c'  # continue running
                current_process.start_time = current_time
            current_time += 1
            current_process.remaining_time -= 1

            # Check if the process is finished
            if current_process.remaining_time == 0:
                current_process.state = 'f'
                current_process.finish_time = current_time
                current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                completed_processes += 1
                self.schedule_queue.append(current_process)
        self.display_results("SRT")


    def round_robin(self, time_quantum):
        queue = deque(self.processes)
        current_time = 0
        while queue:
            current_process = queue.popleft()
            if current_process.arrival_time > current_time:
                current_time = current_process.arrival_time
            
            # Determine the actual time for this slice
            execution_time = min(time_quantum, current_process.remaining_time)
            current_process.remaining_time -= execution_time
            current_process.start_time = current_time
            current_time += execution_time

            if current_process.remaining_time == 0:
                current_process.state = 'f'
                current_process.finish_time = current_time
                current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                self.schedule_queue.append(current_process)
            else:
                queue.append(current_process)  # Re-queue the process to run in the next available turn
        self.display_results("RR")

    def display_results(self, algorithm):
        print(f"{algorithm} Schedule:")
        for p in self.schedule_queue:
            print(f"P{p.number} [{p.start_time}, {p.finish_time}]")
        self.schedule_queue.clear()

def read_processes(filename):
    processes = []
    try:
        with open(filename, 'r') as file:
            next(file)  
            context_switch_time, time_quantum = map(float, next(file).split())
            next(file)  
            for line in file:
                number, arrival, burst = map(int, line.split())
                processes.append(Process(number, arrival, burst))
    except FileNotFoundError:
        print("Error: File not found.")
        sys.exit(1)
    return processes, time_quantum

def main():
    processes, time_quantum = read_processes("Processes.txt")
    scheduler = Scheduler(processes)
    # scheduler.fcfs()
    # scheduler.srt()
    scheduler.round_robin(time_quantum)

if __name__ == "__main__":
    main()
