

import random

from functools import cmp_to_key
from matplotlib import pyplot
# A task instance


class TaskIns(object):

    # Constructor (should only be invoked with keyword parameters)
    def __init__(self, start, end, priority, name):
        self.start = start
        self.end = end
        self.usage = 0
        self.priority = priority
        self.name = int(name)
        self.id = int(random.random() * 10000)

    # Allow an instance to use the cpu (periodic)
    def use(self, usage):
        self.usage += usage
        if self.usage >= self.end - self.start:
            return True
        return False

    # Default representation
    def __repr__(self):
        return str(self.name) + "#" + str(self.id) + " - start: " + str(self.start) + " priority: " + str(self.priority)
        # + budget_text

    # Get name as Name#id
    def get_unique_name(self):
        return str(self.name) + "#" + str(self.id)

# Task types (templates for periodic tasks)


class TaskType(object):

    # Constructor
    def __init__(self, period, release, execution, deadline, name):
        self.period = period
        self.release = release
        self.execution = (int)(execution)
        self.deadline = deadline
        self.name = name

# Priority comparison


def priority_cmp(one, other):
    if one.priority < other.priority:
        return -1
    elif one.priority > other.priority:
        return 1
    return 0

# Deadline monotonic comparison


def tasktype_cmp(self, other):
    if self.deadline < other.deadline:
        return -1
    if self.deadline > other.deadline:
        return 1
    return 0


def plot(sequence_of_process):
    # for i in range(0, len(sequence_of_process)):
    #     print(f"{i}: {sequence_of_process[i]}")
    colors = ['w', 'r', 'b', 'g']
    fig, ax = pyplot.subplots(figsize=(10, 6))
    ax.set_ylim(0, 40)
    ax.set_xlim(0, 300)
    ax.set_xlabel('time')
    xticks = []
    xtickslabel = []
    for i in range(0, 281, 20):
        xticks.append(i)
        xtickslabel.append(i/10)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtickslabel)
    ax.set_yticks([12.5, 22.5, 32.5])
    ax.set_yticklabels(['T1', "T2", "T3"])
    a = 0
    for i in sequence_of_process:
        ax.broken_barh([(a, 5)], (i*10, 5), facecolors=colors[i])
        a = a + 5
    pyplot.show()


if __name__ == '__main__':
    # Variables
    task_types = []
    tasks = []
    sequence_of_process = []
    # Allocate task types
    task_types.append(TaskType(period=40, release=0,
                               execution=15, deadline=40, name=1))
    task_types.append(TaskType(period=100, release=0,
                               execution=30, deadline=100, name=2))
    task_types.append(TaskType(period=120, release=0,
                               execution=30, deadline=120, name=3))

    # Sort types rate monotonic
    task_types = sorted(task_types, key=cmp_to_key(tasktype_cmp))

    period = 280
    # Create task instances
    for i in range(0, period, 5):
        for task_type in task_types:
            if (i - task_type.release) % task_type.period == 0 and i >= task_type.release:
                start = i
                end = start + task_type.execution
                priority = start + task_type.deadline - task_type.execution
                tasks.append(TaskIns(start=start, end=end,
                                     priority=priority, name=task_type.name))

    # Simulate clock
    clock_step = 5
    for i in range(0, period, clock_step):
        # Fetch possible tasks that can use cpu and sort by priority
        possible = []
        for t in tasks:
            if t.start <= i:
                possible.append(t)
        possible = sorted(possible, key=cmp_to_key(priority_cmp))

        # Select task with highest priority
        if len(possible) > 0:
            on_cpu = possible[0]
            sequence_of_process.append(possible[0].name)
            print(f"{i}: {on_cpu.get_unique_name()} uses the processor. "),
            on_cpu.priority += 1
            if on_cpu.use(clock_step):
                tasks.remove(on_cpu)
                print("Finish!"),
        else:
            print('No task uses the processor. ')
        print("\n")

    # Print remaining periodic tasks

    for p in tasks:
        print(p.get_unique_name() + " is dropped due to overload at time: " + str(i))
    plot(sequence_of_process)
    # plot(sequence_of_process)
