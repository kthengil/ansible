#!/usr/bin/env python3

import subprocess
import sys
import tempfile
from pathlib import Path

# =========================
# USER CONFIGURATION
# =========================

RUNTIME = "docker"          # podman or docker
BASE_IMAGE = "rocky9"       # rocky8 or rocky9
ANSIBLE_USER = "sysansible"

CONTROL_IMAGE_SUFFIX = "ansiblecn"
MANAGED_IMAGE_SUFFIX = "ansiblemn"

# =========================
# BASE IMAGE MAP (LOCAL)
# =========================

SUPPORTED_BASE_IMAGES = {
    "rocky8": "rockylinux/rockylinux:8",
    "rocky9": "rockylinux/rockylinux:9",
}

# =========================
# UTILITY FUNCTIONS
# =========================

def run(cmd):
    print(f"[+] {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def runtime_available():
    try:
        subprocess.run(
            [RUNTIME, "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except Exception:
        print(f"[ERROR] Container runtime '{RUNTIME}' not available")
        sys.exit(1)

def image_exists(image):
    result = subprocess.run(
        f"{RUNTIME} image inspect {image}",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

# =========================
# DOCKERFILE GENERATION
# =========================

def generate_dockerfile(base_image, install_ansible=False):
    is_rocky9 = base_image.endswith(":9")

    ansible_install = ""

    if install_ansible:
        if is_rocky9:
            ansible_install = """
RUN dnf install -y ansible-core && dnf clean all
"""
        else:
            ansible_install = """
RUN dnf install -y epel-release \\
    && dnf install -y ansible-core \\
    && dnf clean all
"""

    return f"""
FROM {base_image}

RUN dnf install -y \\
        sudo \\
        openssh-server \\
        openssh-clients \\
        python3 \\
        which \\
    && dnf clean all

RUN ssh-keygen -A

RUN useradd -m {ANSIBLE_USER} \\
    && echo "{ANSIBLE_USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/{ANSIBLE_USER} \\
    && chmod 0440 /etc/sudoers.d/{ANSIBLE_USER}

{ansible_install}

EXPOSE 22

CMD ["/bin/bash", "-c", "rm -f /run/nologin && exec /usr/sbin/sshd -D"]

""".strip()

# =========================
# IMAGE BUILD LOGIC
# =========================

def build_image(base_image, role_suffix):
    image_tag = base_image.split(":")[1]   # 8 or 9
    image_name = f"rocky{image_tag}{role_suffix}"
    install_ansible = role_suffix == CONTROL_IMAGE_SUFFIX

    dockerfile_content = generate_dockerfile(
        base_image=base_image,
        install_ansible=install_ansible
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        dockerfile_path = Path(tmpdir) / "Dockerfile"
        dockerfile_path.write_text(dockerfile_content)

        run(
            f"{RUNTIME} build "
            f"-t {image_name} "
            f"-f {dockerfile_path} "
            f"{tmpdir}"
        )

    print(f"[OK] Built image: {image_name}")

# =========================
# MAIN
# =========================

def main():
    runtime_available()

    if BASE_IMAGE not in SUPPORTED_BASE_IMAGES:
        print(f"[ERROR] Unsupported BASE_IMAGE: {BASE_IMAGE}")
        sys.exit(1)

    base_image = SUPPORTED_BASE_IMAGES[BASE_IMAGE]

    if not image_exists(base_image):
        print(f"[ERROR] Base image not found locally: {base_image}")
        sys.exit(1)

    print(f"[INFO] Runtime      : {RUNTIME}")
    print(f"[INFO] Base Image   : {base_image}")
    print(f"[INFO] Ansible User : {ANSIBLE_USER}")

    build_image(base_image, MANAGED_IMAGE_SUFFIX)
    build_image(base_image, CONTROL_IMAGE_SUFFIX)

    print("\n[SUCCESS] Image build completed successfully")

if __name__ == "__main__":
    main()
