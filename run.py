import sys
import platform
import subprocess
import re
from urllib.request import urlopen
from html.parser import HTMLParser

# --- Configuration ---
# The base URL for the PyTorch nightly builds.
# We will append the CUDA version slug (e.g., 'cu125') to this.
NIGHTLY_INDEX_URL_BASE = "https://download.pytorch.org/whl/nightly/"

# Packages to install
PACKAGES = ["torch", "torchvision", "torchaudio"]
# ---------------------

class NightlyLinkParser(HTMLParser):
    """A simple HTML parser to find wheel links on the nightly index page."""
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)
            if "href" in attrs:
                self.links.append(attrs["href"])

def get_system_info():
    """Gathers necessary system information for finding the correct wheel."""
    py_version = f"cp{sys.version_info.major}{sys.version_info.minor}"
    
    system = platform.system()
    if system == "Windows":
        os_tag = "win"
    elif system == "Linux":
        os_tag = "linux"
    elif system == "Darwin":
        os_tag = "macosx"
    else:
        raise RuntimeError(f"Unsupported OS: {system}")

    architecture = platform.machine().lower()
    if "amd64" in architecture or "x86_64" in architecture:
        arch_tag = "amd64" if system == "Windows" else "x86_64"
    elif "arm64" in architecture or "aarch64" in architecture:
        arch_tag = "arm64"
    else:
        raise RuntimeError(f"Unsupported architecture: {architecture}")

    return py_version, os_tag, arch_tag

def find_compatible_wheel(links, package_name, py_version, os_tag, arch_tag):
    """Finds a compatible wheel URL from a list of links."""
    # Example wheel format: torch-2.9.0.dev20250801%2Bcu125-cp310-cp310-win_amd64.whl
    # We need to match: {package_name}-...-{py_version}-{py_version}-{os_tag}_{arch_tag}.whl
    
    # Regex to capture the package name and the platform tags
    # It looks for the package name, then any characters until the python version,
    # then the python version again, then the os and arch tags.
    pattern = re.compile(
        rf"{package_name}-.*?-"
        rf"{py_version}-{py_version}-"
        rf"{os_tag}_{arch_tag}\.whl"
    )
    
    for link in reversed(links): # Search from newest to oldest
        if pattern.search(link):
            return link
    return None

def main():
    """Main execution function."""
    print("--- PyTorch Nightly Installer ---")

    # 1. Get user's CUDA version
    cuda_version_input = input("Enter your installed CUDA version (e.g., 12.5, 11.8): ").strip()
    if not cuda_version_input:
        print("CUDA version is required.")
        return
    
    cuda_slug = f"cu{cuda_version_input.replace('.', '')}"
    nightly_url = f"{NIGHTLY_INDEX_URL_BASE}{cuda_slug}/"
    
    print(f"[*] Checking index: {nightly_url}")

    # 2. Get system info
    try:
        py_version, os_tag, arch_tag = get_system_info()
        print(f"[*] System Info: Python {py_version}, OS: {os_tag}, Arch: {arch_tag}")
    except RuntimeError as e:
        print(f"Error: {e}")
        return

    # 3. Fetch and parse the nightly index page
    try:
        with urlopen(nightly_url) as response:
            if response.status != 200:
                print(f"Error: Could not fetch URL. Status code: {response.status}")
                print("Please check if the CUDA version is correct and has a nightly build.")
                return
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return

    parser = NightlyLinkParser()
    parser.feed(html)
    
    # 4. Find compatible wheels
    wheels_to_install = []
    for package in PACKAGES:
        print(f"[*] Searching for compatible '{package}' wheel...")
        wheel_path = find_compatible_wheel(parser.links, package, py_version, os_tag, arch_tag)
        if wheel_path:
            wheel_url = f"{nightly_url}/{wheel_path}"
            wheels_to_install.append(wheel_url)
            print(f"  [+] Found: {wheel_path}")
        else:
            print(f"  [-] Warning: No compatible wheel found for '{package}'.")

    if not wheels_to_install:
        print("\nNo compatible packages found. Aborting installation.")
        return

    # 5. Install the packages
    print("\n--- Installation ---")
    print("The following packages will be installed:")
    for url in wheels_to_install:
        print(f"- {url.split('/')[-1]}")
        
    confirm = input("Proceed with installation? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Installation aborted.")
        return

    install_command = [sys.executable, "-m", "pip", "install", "--upgrade"] + wheels_to_install
    
    try:
        print("\nRunning installation command...")
        subprocess.run(install_command, check=True)
        print("\n[SUCCESS] Installation complete.")
        
        # 6. Log the versions
        with open("pytorch_nightly_install.log", "a") as log_file:
            from datetime import datetime
            log_file.write(f"--- Log Entry: {datetime.now()} ---\n")
            log_file.write(f"Installed for CUDA {cuda_version_input} on {os_tag}_{arch_tag} with Python {py_version}\n")
            for url in wheels_to_install:
                log_file.write(f"- {url}\n")
            log_file.write("\n")
        print("Installation details logged to 'pytorch_nightly_install.log'")

    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Installation failed with exit code {e.returncode}.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()