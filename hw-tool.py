import importlib.util
import subprocess

# Funktion zur Überprüfung und Installation von Modulen
def install_module(module_name):
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"{module_name} wird installiert...")
        subprocess.run(["pip", "install", module_name])

# Installiere psutil und GPUtil, wenn sie nicht vorhanden sind
install_module("psutil")
install_module("GPUtil")

import subprocess

# Definieren Sie den Befehl, um setuptools zu installieren
command = ['pip', 'install', 'setuptools']

# Führen Sie den Befehl aus
try:
    subprocess.check_call(command)
    print("setuptools wurde erfolgreich installiert.")
except subprocess.CalledProcessError as e:
    print("Fehler beim Installieren von setuptools:", e)


# Anschließend können Sie die Module importieren und verwenden
import psutil
import GPUtil
from tkinter import *

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

#  # Nach 5 Sekunden erneut aufrufen
#     fenster.after(5000, update_hardware_info)


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

fenster.mainloop()
