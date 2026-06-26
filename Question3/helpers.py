#multithreading test, single-thread test, and graph plotting
import time
from threading import Thread
import matplotlib.pyplot as plt
from factorial import compute_factorial

# ======================================================
# MULTITHREAD TEST
# ======================================================
def run_multithread(numbers, rounds=10):
    #returns a list of times (ns) for each round + the average
    times = []
    for _ in range(rounds):
        threads = []
        start_times = []
        end_times = []

        #the work each thread does
        def worker(num):
            start_times.append(time.time_ns())   #thread start time
            compute_factorial(num)               #the actual factorial work
            end_times.append(time.time_ns())     #thread end time

        #create one thread per factorial number
        for num in numbers:
            t = Thread(target=worker, args=(num,))
            threads.append(t)
            t.start()

        #wait for all threads to finish
        for t in threads:
            t.join()

        #total time = last thread to finish - first thread to start
        total_ns = max(end_times) - min(start_times)
        times.append(total_ns)
    avg = sum(times) / len(times)
    return times, avg

# ======================================================
# SINGLE - THREAD TEST
# ======================================================
def run_singlethread(numbers, rounds=10):
    #same factorials but run one after another in the main thread
    times = []
    for _ in range(rounds):
        start = time.time_ns()
        for num in numbers:
            compute_factorial(num) #run in sequence, no threads
        end = time.time_ns()
        times.append(end - start)
    avg = sum(times) / len(times)
    return times, avg

# ======================================================
# GRAPH PLOTTING
# ======================================================
def plot_results(mt_times, st_times):
    #convert nanoseconds to milliseconds for a readable graph
    mt_ms = [t / 1e6 for t in mt_times]
    st_ms = [t / 1e6 for t in st_times]
    rounds = list(range(1, len(mt_times) + 1))

    #Graph 1: line graph of time per round
    plt.figure(figsize=(8, 5))
    plt.plot(rounds, mt_ms, marker="o", label="Multithread")
    plt.plot(rounds, st_ms, marker="s", label="Single-thread")
    plt.title("Execution Time Per Round")
    plt.xlabel("Round")
    plt.ylabel("Time (ms)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("q3_times_per_round.png", dpi=300)

    #Graph 2: bar chart of average time
    plt.figure(figsize=(6, 5))
    plt.bar(["Multithread", "Single-thread"],
            [sum(mt_ms) / len(mt_ms), sum(st_ms) / len(st_ms)])
    plt.title("Average Execution Time")
    plt.ylabel("Time (ms)")
    plt.tight_layout()
    plt.savefig("q3_average_times.png", dpi=300)

    plt.show()
