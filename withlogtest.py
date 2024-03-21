from tkinter import *
import psutil
import GPUtil
import json
from datetime import datetime
import importlib

def install_module(module_name):
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"{module_name} wird installiert...")
        subprocess.run(["pip", "install", module_name])

# Installiere psutil und GPUtil, wenn sie nicht vorhanden sind
install_module("psutil")
install_module("GPUtil")

# Anschließend können Sie die Module importieren und verwenden
import psutil
import GPUtil

def create_log_file():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"log_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump({}, f, indent=4)
    return filename

def update_hardware_info():
    # CPU-Informationen aktualisieren
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_text.set(f"Anzahl der CPU-Kerne: {cpu_cores}")

    # RAM-Informationen aktualisieren
    ram = psutil.virtual_memory()
    total_ram = ram.total // (1024 ** 3)  # Totaler RAM in GB
    available_ram = ram.available // (1024 ** 3)  # Verfügbarer RAM in GB
    ram_text.set(f"Total: {total_ram} GB\nVerfügbar: {available_ram} GB")

    # Festplatten-Informationen aktualisieren
    disk_partitions = psutil.disk_partitions()
    disk_info = ""
    for partition in disk_partitions:
        disk_usage = psutil.disk_usage(partition.mountpoint)
        disk_info += f"{partition.device} - {partition.mountpoint}\n"
        disk_info += f"Total: {disk_usage.total // (1024 ** 3)} GB\n"
        disk_info += f"Verfügbar: {disk_usage.free // (1024 ** 3)} GB\n\n"
    disk_text.set(disk_info)

    # Netzwerk-Informationen aktualisieren
    net_io_counters = psutil.net_io_counters()
    network_text.set(f"Gesendet: {net_io_counters.bytes_sent // (1024 ** 2)} MB\nEmpfangen: {net_io_counters.bytes_recv // (1024 ** 2)} MB")

    # PCI-Geräte-Informationen aktualisieren
    pci_devices = psutil.disk_io_counters(perdisk=True)
    pci_info = ""
    for device, stats in pci_devices.items():
        pci_info += f"{device}\nLesen: {stats.read_count}\nSchreiben: {stats.write_count}\n\n"
    pci_text.set(pci_info)

    # GPU-Informationen aktualisieren
    gpu_info = ""
    gpus = GPUtil.getGPUs()
    for i, gpu in enumerate(gpus):
        gpu_info += f"GPU {i+1}:\nName: {gpu.name}\nAuslastung: {gpu.load * 100:.2f}%\nSpeicherauslastung: {gpu.memoryUtil * 100:.2f}%\nTemperatur: {gpu.temperature}°C\n\n"
    gpu_text.set(gpu_info)

    # Write hardware information to JSON file with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"log_{timestamp}.json"
    hardware_info = {
        "CPU": {"Cores": cpu_cores},
        "RAM": {"Total": total_ram, "Available": available_ram},
        "Disks": {f"Disk{i+1}": {"Device": partition.device, "Total": disk_usage.total // (1024 ** 3), "Free": disk_usage.free // (1024 ** 3)} for i, (partition, disk_usage) in enumerate(zip(disk_partitions, map(psutil.disk_usage, (partition.mountpoint for partition in disk_partitions))))},
        "Network": {"Sent": net_io_counters.bytes_sent // (1024 ** 2), "Received": net_io_counters.bytes_recv // (1024 ** 2)},
        "PCI Devices": {f"Device{i+1}": {"Read": stats.read_count, "Write": stats.write_count} for i, (device, stats) in enumerate(pci_devices.items())},
        "GPUs": {f"GPU{i+1}": {"Name": gpu.name, "Load": gpu.load * 100, "MemoryUtil": gpu.memoryUtil * 100, "Temperature": gpu.temperature} for i, gpu in enumerate(gpus)}
    }
    with open(filename, 'w') as f:
        json.dump(hardware_info, f, indent=4)

# GUI initialization and layout code remains unchanged

fenster = Tk()
fenster.geometry("800x600")
fenster.title("Hardware-Informationen")

# CPU-Informationen
cpu_frame = LabelFrame(fenster, text="CPU-Informationen")
cpu_frame.pack(padx=10, pady=10, fill="both", expand="yes")
cpu_text = StringVar()
Label(cpu_frame, textvariable=cpu_text).pack()

# RAM-Informationen
ram_frame = LabelFrame(fenster, text="RAM-Informationen")
ram_frame.pack(padx=10, pady=10, fill="both", expand="yes")
ram_text = StringVar()
Label(ram_frame, textvariable=ram_text).pack()

# Festplatten-Informationen
disk_frame = LabelFrame(fenster, text="Festplatten-Informationen")
disk_frame.pack(padx=10, pady=10, fill="both", expand="yes")
disk_text = StringVar()
Label(disk_frame, textvariable=disk_text, justify=LEFT).pack()

# Netzwerk-Informationen
network_frame = LabelFrame(fenster, text="Netzwerk-Informationen")
network_frame.pack(padx=10, pady=10, fill="both", expand="yes")
network_text = StringVar()
Label(network_frame, textvariable=network_text).pack()

# PCI-Geräte-Informationen
pci_frame = LabelFrame(fenster, text="PCI-Geräte-Informationen")
pci_frame.pack(padx=10, pady=10, fill="both", expand="yes")
pci_text = StringVar()
Label(pci_frame, textvariable=pci_text, justify=LEFT).pack()

# GPU-Informationen
gpu_frame = LabelFrame(fenster, text="GPU-Informationen")
gpu_frame.pack(padx=10, pady=10, fill="both", expand="yes")
gpu_text = StringVar()
Label(gpu_frame, textvariable=gpu_text, justify=LEFT).pack()

# Button zum Aktualisieren der Hardware-Informationen
update_button = Button(fenster, text="Aktualisiere Hardware-Informationen", command=update_hardware_info)
update_button.pack(pady=10)

# Initialisieren der Anzeige der Hardware-Informationen
update_hardware_info()

# Create log file at the beginning
create_log_file()

# Tkinter main loop
fenster.mainloop()
