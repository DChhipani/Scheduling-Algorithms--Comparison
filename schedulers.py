from des import SchedulerDES
from event import EventTypes, Event
from process import ProcessStates



class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        # finds the current process in the list and returns it without changing the order
        return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        #runs every current process till termination
        new_time = self.time + cur_process.run_for(cur_process.service_time, self.time)
        process_event_type = EventTypes.PROC_CPU_DONE
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id, event_type=process_event_type, event_time=new_time)
    


class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):
        #because we are finding the shortest job every iteration by finding the minimum service time 
        #findMin algorithm
        min = 0
        result = self.processes[0]
        for process in self.processes:
            if self.time >= process.arrival_time and process.process_state == ProcessStates.READY and (
                    min > process.remaining_time or min == 0):
                result = process
                min = process.remaining_time
        
        return result

    def dispatcher_func(self, cur_process):
        # runs the shortest program on arrival to completion
        new_time = self.time + cur_process.run_for(cur_process.service_time, self.time)
        process_event_type = EventTypes.PROC_CPU_DONE
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id, event_type=process_event_type, event_time=new_time)
        
class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        # logic as FCFS
        return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        # runs each process for a select amount of time i.e. quantum
        new_time = self.time + cur_process.run_for(self.quantum, self.time)
        if cur_process.remaining_time > 0:
            process_event_type = EventTypes.PROC_CPU_REQ
            cur_process.process_state = ProcessStates.READY
        else:
            process_event_type = EventTypes.PROC_CPU_DONE
            cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id, event_type=process_event_type, event_time=new_time)


class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):
        # repeats what is done in SJF
        min = 0
        result = self.processes[0]
        for process in self.processes:
            if self.time >= process.arrival_time and process.process_state == ProcessStates.READY and (
                    min > process.remaining_time or min == 0):
                result = process
                min = process.remaining_time
            return result
    

    def dispatcher_func(self, cur_process):
        # every time a change occurs it checks to see what is the shortest remaining time and keeps doing it
        # until it has looped through everything
        process_time = self.next_event_time() - self.time
        new_time = self.time + cur_process.run_for(process_time, self.time)
        if cur_process.remaining_time > 0:
            process_event_type = EventTypes.PROC_CPU_REQ
            cur_process.process_state = ProcessStates.READY
        else:
            process_event_type = EventTypes.PROC_CPU_DONE
            cur_process.process_state = ProcessStates.TERMINATED
            return Event(process_id=cur_process.process_id, event_type=process_event_type, event_time=new_time)
            
