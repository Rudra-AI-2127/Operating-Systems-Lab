def fcfs(processes):
    current_time = 0
    intervals = []

    ordered = sorted(
        processes,
        key=lambda p: (p["arrival"], p["pid"])
    )

    for process in ordered:
        if current_time < process["arrival"]:
            intervals.append(
                ("IDLE", current_time, process["arrival"])
            )
            current_time = process["arrival"]

        start = current_time
        end = start + process["burst"]

        intervals.append(
            (process["pid"], start, end)
        )

        current_time = end

    return intervals


def sjf(processes):
    remaining = processes.copy()
    current_time = 0
    intervals = []

    while remaining:
        ready = [
            p for p in remaining
            if p["arrival"] <= current_time
        ]

        if not ready:
            next_arrival = min(
                p["arrival"] for p in remaining
            )
            intervals.append(
                ("IDLE", current_time, next_arrival)
            )
            current_time = next_arrival
            continue

        p = min(
            ready,
            key=lambda x: (x["burst"], x["arrival"], x["pid"])
        )

        start = current_time
        end = start + p["burst"]

        intervals.append((p["pid"], start, end))

        current_time = end
        remaining.remove(p)

    return intervals


def print_result(title, result):
    print("\n" + title)
    print("Process Start End")

    for item in result:
        print(item[0], item[1], item[2])

    sequence = [item[0] for item in result]
    print("Sequence:", " -> ".join(sequence))


print("FCFS AND SJF SCHEDULING")

while True:
    try:
        n = int(input("Enter number of processes: "))
        if n <= 0:
            print("Number of processes must be positive.")
            continue
        break
    except ValueError:
        print("Please enter a valid integer.")

processes = []

for i in range(n):
    pid = f"P{i + 1}"

    while True:
        try:
            arrival = int(input(f"Enter Arrival Time for {pid}: "))
            if arrival < 0:
                print("Arrival Time cannot be negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    while True:
        try:
            burst = int(input(f"Enter Burst Time for {pid}: "))
            if burst <= 0:
                print("Burst Time must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    processes.append({
        "pid": pid,
        "arrival": arrival,
        "burst": burst
    })

print("\nINPUT PROCESSES")
print("PID\tArrival\tBurst")

for p in processes:
    print(
        p["pid"],
        p["arrival"],
        p["burst"],
        sep="\t"
    )

print_result("\nFCFS SCHEDULING", fcfs(processes))
print_result("\nSJF SCHEDULING", sjf(processes))
