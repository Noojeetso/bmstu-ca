from approximation_tools import *

is_running = True


def get_menu_num() -> int:
    num_str = input("Enter menu number: ")
    num = int(num_str)
    if num < 0 or num > 3:
        raise ValueError
    return num


def menu():
    global is_running
    print("1 - approximation")
    print("2 - root finding")
    print("3 - solve equation")
    print("0 - exit")

    try:
        num = get_menu_num()
    except ValueError:
        print("Incorrect menu number\n")
        return

    if num == 0:
        is_running = False
    if num == 1:
        compare_approximation()
    if num == 2:
        compare_root_finding()
    if num == 3:
        solve_equations()
    print("")


if __name__ == "__main__":
    while is_running:
        menu()
