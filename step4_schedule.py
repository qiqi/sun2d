import collections
from numpy import *

def construct_neighbors(ij_pairs):
    in_nodes = collections.defaultdict(set)
    out_nodes = collections.defaultdict(set)
    for i, j in ij_pairs:
        in_nodes[j].add(i)
        out_nodes[i].add(j)
    return in_nodes, out_nodes

class CommunicationCostModel:
    comm_cost_const = 20000
    comm_cost_slope = 0

    def __init__(self, area_dict):
        self.const_area_dict = area_dict
        self.in_nodes, self.out_nodes = construct_neighbors(area_dict.keys())

    def __call__(self, i, j):
        return self.const_area_dict[(i,j)] * self.comm_cost_slope \
                + self.comm_cost_const

def compute_static_level(volume_dict, area_dict, comm_cost):
    level = {i: volume_dict[i] for i in volume_dict}
    active = set(volume_dict).difference(set(comm_cost.out_nodes))
    while active:
        j = active.pop()
        if j in comm_cost.in_nodes:
            for i in comm_cost.in_nodes[j]:
                level[i] = max(level[i],
                               level[j] + comm_cost(i,j) + volume_dict[i])
                active.add(i)
    return level

class TaskQueue:
    def __init__(self, proc_id, volume_dict, comm_cost, processor_assigned):
        self.proc_id = proc_id
        self.tasks = []
        self.start_time = {}
        self.const_volume_dict = volume_dict
        self.const_comm_cost = comm_cost
        self.processor_assigned = processor_assigned

    def earliest_start_time(self, task):
        assert task not in processor_assigned and task not in self.start_time
        in_nodes = self.const_comm_cost.in_nodes
        earliest_start_time = 0
        for prev_task in in_nodes[task]:
            prev_task_processor = self.processor_assigned[prev_task]
            if prev_task_processor is not self:
                earliest_start_time = max(earliest_start_time,
                        prev_task_processor.start_time[prev_task] +
                        self.const_comm_cost(prev_task, task))
        return max(earliest_start_time, self.next_available_time)

    def add(self, task):
        self.start_time[task] = self.earliest_start_time(task)
        self.tasks.append(task)
        processor_assigned[task] = self

    @property
    def next_available_time(self):
        if self.tasks:
            last_task = self.tasks[-1]
            return self.start_time[last_task] + volume_dict[last_task]
        else:
            return 0

tasks, volume = loadtxt('outputs/volume.txt', dtype=int).T
task_i, task_j, area = loadtxt('outputs/connectivity.txt', dtype=int).T

volume_dict = {i: v for i, v in zip(tasks, volume)}
area_dict = {(i,j) : a for i, j, a in zip(task_i, task_j, area)}

comm_cost = CommunicationCostModel(area_dict)
static_level = compute_static_level(volume_dict, area_dict, comm_cost)

processor_assigned = {}
processors = [TaskQueue(i, volume_dict, comm_cost, processor_assigned)
              for i in range(8)]

in_nodes, out_nodes = construct_neighbors(zip(task_i, task_j))
remaining_tasks = {task: len(in_nodes[task]) if task in in_nodes else 0
                   for task in tasks}

for i in range(len(processors)):
    start_task = 2**(i + 8)
    del remaining_tasks[start_task]
    processors[i].add(start_task)
    for future_task in out_nodes[start_task]:
        remaining_tasks[future_task] -= 1

while remaining_tasks:
    ready_tasks = [t for t in remaining_tasks if remaining_tasks[t] == 0]
    i_task = argmax([static_level[i] for i in ready_tasks])
    task = ready_tasks[i_task]
    del remaining_tasks[task]
    start_times = [p.earliest_start_time(task) for p in processors]
    processors[argmin(start_times)].add(task)
    for future_task in out_nodes[task]:
        remaining_tasks[future_task] -= 1

with open('outputs/processor_assignment.txt', 'wt') as fh:
    for task, p in processor_assigned.items():
        fh.write('{:16d} {:d}\n'.format(task, p.proc_id))
for p in processors:
    fname = 'outputs/processor_{}_schedule.txt'.format(p.proc_id)
    with open(fname, 'wt') as fh:
        for task in p.tasks:
            fh.write('{:16d} {:d}\n'.format(task, p.start_time[task]))
