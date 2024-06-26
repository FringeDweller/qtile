import os
import shutil
import subprocess
from datetime import datetime

def backup_config():
    print("Backing up qtile, dunst, and picom folders...")
    config_path = os.path.expanduser("~/.config")
    backup_folder = os.path.join(config_path, "backup")
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    backup_path = os.path.join(backup_folder, f"backup_{timestamp}")
    folders_to_backup = [
        os.path.expanduser("~/.config/.bashrc"),
        os.path.expanduser("~/.config/qtile"),
        os.path.expanduser("~/.config/dunst"),
        os.path.expanduser("~/.config/picom"),
        os.path.expanduser("~/.config/rofi"),
        os.path.expanduser("~/.config/alacritty"),
        os.path.expanduser("~/.config/nano")
    ]
    try:
        os.makedirs(backup_path, exist_ok=True)
        for folder in folders_to_backup:
            if os.path.exists(folder):
                shutil.move(folder, backup_path)
                print(f"Moved folder: {folder} to {backup_path}")
            else:
                print(f"Folder {folder} does not exist. Skipping backup...")
    except shutil.Error as e:
        print(f"Error moving directory: {e}")



def overwrite_pacman_conf():
    try:
        # Path to source and destination files
        source_file = os.path.expanduser("~/dots/scripts/pacman.conf")
        destination_file = "/etc/pacman.conf"

        # Use sudo to overwrite the destination file with the content of the source file
        subprocess.run(['sudo', 'cp', source_file, destination_file], check=True)
        print(f"File {destination_file} overwritten successfully with sudo.")
    except subprocess.CalledProcessError as e:
        print(f"Error overwriting file: {e}")
        

def check_packages():
    print("Checking and installing necessary packages...")
    packages = [
        "git", "xorg", "xorg-xinit", "picom", "alacritty", "gtk3", "arc-gtk-theme",
        "dunst", "neofetch", "qemu-full", "virt-manager", "rofi", "pavucontrol", "pipewire-alsa",
        "pipewire-pulse", "virt-viewer", "dnsmasq", "bridge-utils", "libguestfs", "ebtables", "vde2",
        "openbsd-netcat","openssh", "feh", "mc", "alsa-utils", "python-pywal", "variety",
        "thunar", "nerd-fonts", "nano", "nano-syntax-highlighting", "udiskie"
    ]
    for package in packages:
        installed = subprocess.run(['sudo', 'pacman', '-Q', package], capture_output=True)
        if installed.returncode != 0:
            print(f"{package} is not installed. Installing...")
            subprocess.run(['sudo', 'pacman', '-S', '--needed', package])


def check_paru():
    print("Checking and installing Paru...")
    if subprocess.run(['pacman', '-Q', 'paru']).returncode != 0:
        subprocess.run(['git', 'clone', 'https://aur.archlinux.org/paru.git', '/tmp/paru'])
        os.chdir("/tmp/paru")
        subprocess.run(['makepkg', '-si'])


def check_optional_packages():
    print("Checking and installing optional packages...")
    optional_packages = [
        "vscodium-bin", "udisks2", "gvfs", "vscodium-bin", "netbird-bin", "nomachine",
        "ffmpegthumbnailer", "unarchiver", "jq", "poppler", "fd", "ripgrep", "pika-backup",
        "fzf", "zoxide", "brave-bin", "python-psutil", "python-pulsectl-asyncio", "qtile-extras"
    ]
    for package in optional_packages:
        installed = subprocess.run(['sudo', 'pacman', '-Q', package], capture_output=True)
        if installed.returncode != 0:
            print(f"{package} is not installed. Installing...")
            subprocess.run(['paru', '-S', "--needed", package])


def check_ssh():
    print("Checking and enabling SSH service...")
    subprocess.run(['sudo', 'pacman', '-S', '--needed', 'openssh'])
    subprocess.run(['sudo', 'systemctl', 'enable', 'sshd'])
    subprocess.run(['sudo', 'systemctl', 'start', 'sshd'])


def install_netbird_service():
    try:
        print("Installing Netbird service...")
        subprocess.run(['sudo', 'netbird', 'service', 'install'], check=True)
        print("Netbird service installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing Netbird service: {e}")

def start_netbird_service():
    try:
        print("Starting Netbird service...")
        subprocess.run(['sudo', 'netbird', 'service', 'start'], check=True)
        print("Netbird service started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting Netbird service: {e}")


def install_rofi_themes():
    print("Installing Rofi themes...")
    subprocess.run(['git', 'clone', '--depth=1', 'https://github.com/adi1090x/rofi.git'])
    os.chdir('rofi')  # Change the working directory to 'rofi'
    subprocess.run(['chmod', '+x', 'setup.sh'])
    subprocess.run(['./setup.sh'])
    os.chdir('..')  # Change back to the parent directory
    shutil.rmtree('rofi')  # Remove the rofi folder
    

def create_folders():
    print("Creating folders...")
    folders_to_create = [
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Pictures")
    ]
    for folder in folders_to_create:
        os.makedirs(folder, exist_ok=True)


def copy_files():
    print("Copying files...")
    files_to_copy = [
        os.path.expanduser("~/dots/scripts/.bashrc")
    ]
    for file_path in files_to_copy:
        dest = os.path.expanduser("~/.config")
        try:
            shutil.copy(file_path, dest)
            print(f"File copied: {file_path} to {dest}")
        except FileNotFoundError:
            print(f"Source file not found: {file_path}")
        except FileExistsError:
            print(f"File already exists at destination: {dest}")


def copy_folders():
    print("Copying folders...")
    folders_to_copy = [
        ("~/dots/wallpaper", "~/Pictures/wallpapers"),
        ("~/dots/qtile", "~/.config/qtile"),
        ("~/dots/dunst", "~/.config/dunst"),
        ("~/dots/picom", "~/.config/picom"),
        ("~/dots/alacritty", "~/.config/alacritty"),
        ("~/dots/nano", "~/.config/nano")
    ]
    for src, dest in folders_to_copy:
        src = os.path.expanduser(src)
        dest = os.path.expanduser(dest)
        try:
            shutil.copytree(src, dest)
            print(f"Folder copied: {src} to {dest}")
        except FileNotFoundError:
            print(f"Source folder not found: {src}")
        except FileExistsError:
            print(f"Folder already exists at destination: {dest}")


def make_autostart_executable():
    autostart_file = os.path.expanduser("~/.config/qtile/autostart.sh")
    if os.path.exists(autostart_file):
        os.chmod(autostart_file, 0o755)  # Change file permissions to make it executable
        print(f"Made {autostart_file} executable.")
    else:
        print(f"File {autostart_file} not found. Skipping...")


def set_gtk_theme(theme_name):
    try:
        # Check if entry exists
        grep_command = f"grep -q 'GTK_THEME={theme_name}' /etc/environment"
        grep_process = subprocess.run(grep_command, shell=True, capture_output=True, text=True)
        if grep_process.returncode == 0:
            print(f"The GTK_THEME={theme_name} entry already exists.")
            return

        # Add entry
        echo_command = f"echo 'GTK_THEME={theme_name}' | sudo tee -a /etc/environment"
        subprocess.run(echo_command, shell=True, check=True)
        print(f"GTK_THEME={theme_name} added successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting GTK theme: {e}")

def main():
    backup_config()
    overwrite_pacman_conf()
    check_packages()
    check_paru()
    check_optional_packages()
    check_ssh()
    install_netbird_service()
    start_netbird_service()
    install_rofi_themes()
    create_folders()
    copy_files()
    copy_folders()
    make_autostart_executable()
    set_gtk_theme("Arc-Dark")

if __name__ == "__main__":
    main()
