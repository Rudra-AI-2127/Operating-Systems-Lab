from threading import Thread, current_thread
from multiprocessing import Process, Pipe, Value


# -----------------------------
# PROCESS DATA
# -----------------------------

processes = [
    {"pid": "P1", "arrival": 0, "burst": 7},
    {"pid": "P2", "arrival": 2, "burst": 4},
    {"pid": "P3", "arrival": 4, "burst": 1},
    {"pid": "P4", "arrival": 5, "burst": 4},
]

intervals = [
    ("P1", 0, 2),
    ("P2", 2, 4),
    ("P1", 4, 6),
    ("P3", 6, 7),
    ("P2", 7, 9),
    ("P4", 9, 11),
    ("P1", 11, 13),
    ("P4", 13, 15),
    ("P1", 15, 16)
]


# -----------------------------
# PART A: SCHEDULING METRICS
# -----------------------------

def calculate_metrics():
    print("\n--- SCHEDULING METRICS ---")
    print("PID AT BT CT TAT WT RT")

    tat_total = 0
    wt_total = 0
    rt_total = 0

    for p in processes:
        runs = [x for x in intervals if x[0] == p["pid"]]

        first_start = runs[0][1]
        completion = runs[-1][2]

        tat = completion - p["arrival"]
        wt = tat - p["burst"]
        rt = first_start - p["arrival"]

        tat_total += tat
        wt_total += wt
        rt_total += rt

        print(
            p["pid"],
            p["arrival"],
            p["burst"],
            completion,
            tat,
            wt,
            rt
        )

    n = len(processes)

    print("Average TAT =", round(tat_total / n, 2))
    print("Average WT =", round(wt_total / n, 2))
    print("Average RT =", round(rt_total / n, 2))


# -----------------------------
# PART B: GANTT CHART
# -----------------------------

def show_gantt_chart():
    print("\n--- ROUND ROBIN GANTT CHART ---")

    print(" | ".join(pid for pid, _, _ in intervals))

    times = [intervals[0][1]] + [
        end for _, _, end in intervals
    ]

    print(" ".join(str(t) for t in times))


# -----------------------------
# PART C: THREADS
# -----------------------------

def thread_task(name):
    print(
        name,
        "running | Thread ID:",
        current_thread().ident
    )


def thread_demo():
    print("\n--- THREAD DEMO ---")

    t1 = Thread(
        target=thread_task,
        args=("Thread 1",)
    )

    t2 = Thread(
        target=thread_task,
        args=("Thread 2",)
    )

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Both threads completed.")


# -----------------------------
# PART D: PIPE IPC
# -----------------------------

def child_pipe(conn):
    conn.send("Hello Parent - message from Child")
    conn.close()


def pipe_demo():
    print("\n--- PIPE IPC DEMO ---")

    parent_conn, child_conn = Pipe()

    child = Process(
        target=child_pipe,
        args=(child_conn,)
    )

    child.start()

    message = parent_conn.recv()

    child.join()

    print("Parent received:", message)


# -----------------------------
# PART E: SHARED MEMORY
# -----------------------------

def update_shared(value):
    value.value += 10


def shared_memory_demo():
    print("\n--- SHARED MEMORY DEMO ---")

    shared_value = Value("i", 5)

    print(
        "Before child process:",
        shared_value.value
    )

    child = Process(
        target=update_shared,
        args=(shared_value,)
    )

    child.start()
    child.join()

    print(
        "After child process :",
        shared_value.value
    )


# -----------------------------
# MAIN PROGRAM
# -----------------------------

if __name__ == "__main__":
    calculate_metrics()
    show_gantt_chart()
    thread_demo()
    pipe_demo()
    shared_memory_demo()
