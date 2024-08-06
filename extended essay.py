import time
from multiprocess import Pool
import psutil

def cpu_bound_task(start, end):
    """Function to perform a CPU-bound task (sum of squares) over a range."""
    total = 0
    for i in range(start, end):
        total += i * i
    return total

def single_threaded(n):
    """Single-threaded execution of the CPU-bound task."""
    start_time = time.time()
    result = cpu_bound_task(0, n)
    end_time = time.time()
    return end_time - start_time, result

def multi_process(n, num_processes):
    """Multi-process execution of the CPU-bound task using multiprocess."""
    chunk_size = n // num_processes
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_processes)]
    if n % num_processes != 0:
        ranges[-1] = (ranges[-1][0], n)

    start_time = time.time()
    with Pool(processes=num_processes) as pool:
        results = pool.starmap(cpu_bound_task, ranges)
    end_time = time.time()

    total_result = sum(results)
    return end_time - start_time, total_result

def measure_cpu_utilization():
    """Measure CPU utilization over a short period."""
    return psutil.cpu_percent(interval=1)

def run_experiment(n, num_processes_list):
    """Run the experiment with single-threaded and multi-process approaches."""
    results = []

    # Single-threaded approach
    time_taken, result = single_threaded(n)
    cpu_utilization = measure_cpu_utilization()
    results.append({
        'approach': 'Single-threaded',
        'processes': 1,
        'execution_time': time_taken,
        'cpu_utilization': cpu_utilization,
        'result': result
    })

    # Multi-process approach with different number of processes
    for num_processes in num_processes_list:
        time_taken, result = multi_process(n, num_processes)
        cpu_utilization = measure_cpu_utilization()
        results.append({
            'approach': 'Multi-process',
            'processes': num_processes,
            'execution_time': time_taken,
            'cpu_utilization': cpu_utilization,
            'result': result
        })

    return results

# Parameters for the experiment
n = 10**7  # Task size
num_processes_list = [1, 2, 4, 8]  # Different numbers of processes to test

# Run the experiment
experiment_results = run_experiment(n, num_processes_list)

# Display the results
for result in experiment_results:
    print(result)
