from helpers import run_multithread, run_singlethread, plot_results

def concurrent_system():
    factorial_numbers = [50, 100, 200]
    rounds = 10

    print("\n==================================================")
    print("               Concurrent Process Test            ")
    print("==================================================")
    print(f"Numbers: {factorial_numbers}")
    print(f"Rounds : {rounds}")

    while True:
        print("\n==================================================")
        print("              Concurrent Process Menu             ")
        print("==================================================")
        print("1. Multithreading Test")
        print("2. Single-thread Test")
        print("3. Summary + Graph")
        print("4. Exit\n")

        while True:
            choice = input("Enter choice: ").strip()
            if choice in ("1", "2", "3", "4"):
                break
            print("\nInvalid choice. Please enter 1-4 only.")

        if choice == "1":
            print("\n==================================================")
            print("              Multithreading Result               ")
            print("==================================================")
            mt_times, mt_avg = run_multithread(factorial_numbers, rounds)
            for i, t in enumerate(mt_times, 1):
                print(f"Round {i:02d}: {t:,} ns")
            print(f"\nTotal   : {sum(mt_times):,} ns")
            print(f"Average : {mt_avg:,.0f} ns")

        elif choice == "2":
            print("\n==================================================")
            print("              Single - thread Result              ")
            print("==================================================")
            st_times, st_avg = run_singlethread(factorial_numbers, rounds)
            for i, t in enumerate(st_times, 1):
                print(f"Round {i:02d}: {t:,} ns")
            print(f"\nTotal   : {sum(st_times):,} ns")
            print(f"Average : {st_avg:,.0f} ns")


        elif choice == "3":
            print("\n======================================================")
            print("             Multithread vs Single-thread             ")
            print("======================================================")
            mt_times, mt_avg = run_multithread(factorial_numbers, rounds)
            st_times, st_avg = run_singlethread(factorial_numbers, rounds)

            print(f"{'Round':<12}{'Multithread (ns)':<22}{'Single-thread (ns)':<20}")
            print("-" * 54)
            for i, (mt, st) in enumerate(zip(mt_times, st_times), 1):
                print(f"Round {i:02d}  {mt:>18,}    {st:>18,}")

            print("-" * 54)
            print(f"{'Total':<10}{sum(mt_times):>18,}    {sum(st_times):>18,}")
            print(f"{'Average':<10}{mt_avg:>18,.0f}    {st_avg:>18,.0f}")
            print("-" * 54)

            #summary
            if st_avg > 0:
                ratio = (mt_avg / st_avg) * 100
                print(f"\nMultithread takes {ratio:.2f}% of the single-thread time.")
            plot_results(mt_times, st_times)

        elif choice == "4":
            print("\n==================================================")
            print("                     Exiting                      ")
            print("==================================================")
            break

if __name__ == "__main__":
    concurrent_system()
