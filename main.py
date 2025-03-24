import GPUtil
import platform
import psutil
import plotille
import os
import time
import curses

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
def get_system_info():
    print('Getting system info...')
    system_info = {
        "name": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.machine()
    }
    return system_info

def get_gpu_info():
    print('Getting GPU info...')
    gpus = GPUtil.getGPUs()
    gpu_info = [] 
    if not gpus:
        return "No GPUs found"
    else:
        for gpu in gpus:
            gpu_info.append({
                "id": gpu.id,
                "name": gpu.name,
                "memory_total": gpu.memoryTotal,
                "memory_free": gpu.memoryFree,
                "utilization": gpu.load * 100,
            })
    return gpu_info 

def get_memory_info():
    print('Getting memory info...')
    return  {
        "total": psutil.virtual_memory().total,
        "available": psutil.virtual_memory().available,
        "percent": psutil.virtual_memory().percent
    }

def get_disk_info():
    print('Getting disk info...')
    return {
        "total": psutil.disk_usage('/').total,
        "used": psutil.disk_usage('/').used,
        "free": psutil.disk_usage('/').free,
    }


def show_memory_info(stdscr):
    """Display the memory information in the terminal"""
    memory = get_memory_info()

    stdscr.clear()
    stdscr.addstr(0, 0, "Memory Information:\n")
    stdscr.addstr(f"Total Memory: {memory['total'] / (1024 ** 3):.2f} GB\n")
    stdscr.addstr(f"Available Memory: {memory['available'] / (1024 ** 3):.2f} GB\n")
    stdscr.addstr(f"Memory Usage: {memory['percent']}%\n")
    
    stdscr.addstr("\nPress any key to return to menu...")
    stdscr.refresh()
    stdscr.getch()  

def show_system_info(stdscr):
    system = get_system_info()

    stdscr.clear()
    stdscr.addstr(0, 0, "System Information:\n")
    stdscr.addstr(f"System: {system['name']}\n")
    stdscr.addstr(f"Release: {system['release']}\n")
    stdscr.addstr(f"Version: {system['version']}\n")
    stdscr.addstr(f"architecture: {system['architecture']}\n")

    stdscr.addstr("\nPress any key to return to menu...")
    stdscr.refresh()
    stdscr.getch()  


def get_cpu_temp_graph():
    """Display the CPU temperature graph for the last 1 minute"""
    temps = []
    n = []
    i = 0
    while True:
        n.append(i)
        temps.append(round(psutil.cpu_percent(interval=1), 1))

        if len(n) > 60:
            n.pop(0)
            temps.pop(0)

        os.system('cls' if os.name == 'nt' else 'clear')

        fig = plotille.Figure()
        fig.width = 60
        fig.height = 30
        fig.x_label = "Time"
        fig.y_label = "Temperature"
        fig.plot(n, temps, interp="linear", lc="cyan")
        print(fig.show())
        
        print('Current Temperature:', temps[-1], '°C')
        i += 1
        time.sleep(1)

def display_menu(stdscr, selected_index, options):
    """Display the menu with the selected option highlighted"""
    stdscr.clear()  # Clear the screen
    height, width = stdscr.getmaxyx()

    # Title of the menu
    stdscr.addstr(0, 0, "Simple Menu (Use Arrow keys to navigate, Enter to select)")

    for idx, option in enumerate(options):
        x = width // 2 - len(option) // 2  # Centering the options
        y = height // 2 - len(options) // 2 + idx

        if idx == selected_index:
            stdscr.attron(curses.color_pair(1))  # Highlight the selected option
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(1))  # Remove highlight after printing
        else:
            stdscr.addstr(y, x, option)

    stdscr.refresh()


def main(stdscr):
    """Main function that runs the menu loop"""
    curses.curs_set(0)  # Hide the cursor
    curses.start_color()  # Start color functionality
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)  # Color pair for highlighting

    options = ["System Info", "Memory info", "Exit"]
    selected_index = 0

    while True:
        display_menu(stdscr, selected_index, options)

        key = stdscr.getch()  # Get the key press from user
        
        if key == curses.KEY_UP and selected_index > 0:
            selected_index -= 1
        elif key == curses.KEY_DOWN and selected_index < len(options) - 1:
            selected_index += 1
        elif key == 10:  # Enter key
            if selected_index == 0:
                show_system_info(stdscr)
            elif selected_index == 1:
                show_memory_info(stdscr)
            elif options[selected_index] == "Exit":
                break

        clear_screen()
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
