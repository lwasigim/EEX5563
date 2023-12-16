import tkinter as tk
from tkinter import ttk, messagebox

class Process:
    def __init__(self, pid, priority, burst_time):
        """Initialize a process with given parameters."""
        self.pid = pid
        self.priority = priority
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.wait_time = 0

class MultilevelQueueScheduler:
    def __init__(self, num_queues):
        """Initialize a multilevel queue scheduler with a given number of queues."""
        self.queues = [[] for _ in range(num_queues)]
        self.time_quantum = 2
        self.age_threshold = 5

    def enqueue_process(self, process):
        """Add a process to the scheduler's queue based on its priority."""
        self.queues[process.priority].append(process)

    def run_scheduler(self):
        """Run the multilevel queue scheduler."""
        time_elapsed = 0

        while any(queue for queue in self.queues):
            for i in range(len(self.queues)):
                if self.queues[i]:
                    current_process = self.queues[i].pop(0)
                    print(f"Running process {current_process.pid} from Queue {i}")

                    if current_process.remaining_time <= self.time_quantum:
                        time_elapsed += current_process.remaining_time
                        current_process.remaining_time = 0
                    else:
                        time_elapsed += self.time_quantum
                        current_process.remaining_time -= self.time_quantum

                    current_process.wait_time += time_elapsed

                    # Aging mechanism
                    if time_elapsed % self.age_threshold == 0:
                        self.boost_priority(current_process)

                    if current_process.remaining_time > 0:
                        self.queues[i].append(current_process)

        print(f"Total time elapsed: {time_elapsed}")
        return time_elapsed

    def boost_priority(self, process):
        """Increase the priority of a process, capped at the highest priority."""
        process.priority = min(process.priority + 1, len(self.queues) - 1)

class SchedulerApp:
    def __init__(self, master):
        """Initialize the GUI for the scheduler application."""
        self.master = master
        self.master.title("Multilevel Queue Scheduler")

        self.num_queues_var = tk.IntVar(value=3)
        self.time_quantum_var = tk.IntVar(value=2)

        self.create_widgets()

    def create_widgets(self):
        """Create widgets for the GUI."""
        # Process entry
        ttk.Label(self.master, text="Processes (Process ID, Priority, Burst Time):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.process_entry = tk.Text(self.master, height=10, width=40)
        self.process_entry.grid(row=1, column=0, rowspan=3, pady=5)

        # Num Queues entry
        ttk.Label(self.master, text="Number of Queues:").grid(row=0, column=1, sticky=tk.W, pady=5)
        self.num_queues_entry = ttk.Entry(self.master, textvariable=self.num_queues_var)
        self.num_queues_entry.grid(row=1, column=1, pady=5)

        # Time Quantum entry
        ttk.Label(self.master, text="Time Quantum:").grid(row=2, column=1, sticky=tk.W, pady=5)
        self.time_quantum_entry = ttk.Entry(self.master, textvariable=self.time_quantum_var)
        self.time_quantum_entry.grid(row=3, column=1, pady=5)

        # Run button
        ttk.Button(self.master, text="Run Scheduler", command=self.run_scheduler).grid(row=4, column=0, columnspan=2, pady=10)

    def run_scheduler(self):
        """Run the scheduler based on user inputs."""
        try:
            num_queues = self.num_queues_var.get()
            time_quantum = self.time_quantum_var.get()

            # Parse processes from the entry
            processes_text = self.process_entry.get("1.0", tk.END)
            processes_lines = processes_text.split("\n")
            processes = []

            for line in processes_lines:
                if line.strip():
                    pid, priority, burst_time = map(int, line.strip().split(","))
                    processes.append(Process(pid, priority, burst_time))

            scheduler = MultilevelQueueScheduler(num_queues=num_queues)
            scheduler.time_quantum = time_quantum

            for process in processes:
                scheduler.enqueue_process(process)

            total_time_elapsed = scheduler.run_scheduler()

            # Display results in a new window
            self.display_results(total_time_elapsed)

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your input values.")

    def display_results(self, total_time_elapsed):
        """Display scheduling results in a new window."""
        result_window = tk.Toplevel(self.master)
        result_window.title("Scheduler Results")

        result_label = ttk.Label(result_window, text=f"Total time elapsed: {total_time_elapsed}")
        result_label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
