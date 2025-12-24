#!/usr/bin/env python3
"""
ansible_lab.py
Final – Cleaned + Corrected

Lifecycle manager for Ansible Lab using container runtime (docker/podman)

Commands:
    build   – Build images only
    setup   – First-time full bootstrap (creates containers, SSH setup, UX)
    start   – Start existing containers only (no creation)
    stop    – Stop running containers
    decom   – Stop + remove containers + remove network
    status  – Show runtime state
    info    – Show config YAML parsed
"""

import subprocess
import sys
import yaml
from pathlib import Path
from textwrap import indent

CONFIG_FILE = "lab_config.yaml"

# ==========================================================
# UI / UX CONSTANTS
# ==========================================================

class UI:
    RESET  = "\033[0m"
    RED    = "\033[1;31m"
    GREEN  = "\033[1;32m"
    YELLOW = "\033[1;33m"
    CYAN   = "\033[1;36m"

    ICON_CONTROL = "🧠"
    ICON_MANAGED = "🖥️"

    ICON_OK   = "✅"
    ICON_WARN = "⚠️"
    ICON_ERR  = "❌"
    ICON_RUN  = "⚡"
    ICON_STOP = "🛑"
    ICON_DECOM = "🧹"     

    NODE_W  = 12
    ROLE_W  = 8
    STAT_W  = 18


# ==========================================================
# UTILS
# ==========================================================

def node_role(node):
    return ("CONTROL", UI.ICON_CONTROL) if node == CONFIG["control_node"] else ("MANAGED", UI.ICON_MANAGED)

def section(title):
    print(f"\n{UI.CYAN}{title}{UI.RESET}")
    print("-" * 60)

def row(*cols):
    print(" ".join(cols))

def run(cmd, check=True):
    print(f"[+] {cmd}")
    return subprocess.run(cmd, shell=True, check=check)

def load_config():
    if not Path(CONFIG_FILE).exists():
        print(f"[ERROR] Config file not found: {CONFIG_FILE}")
        sys.exit(1)
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)

def runtime():
    return CONFIG["runtime"]

def container_name(node):
    return f"{CONFIG['naming']['prefix']}-{node['name']}"


# ==========================================================
# NETWORK
# ==========================================================

def ensure_network():
    net = CONFIG["network"]["name"]
    r = runtime()
    result = subprocess.run(f"{r} network inspect {net}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode != 0:
        run(f"{r} network create {net}")


# ==========================================================
# CONTAINER EXISTENCE
# ==========================================================

def container_exists(name):
    r = runtime()
    result = subprocess.run(f"{r} inspect {name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0


# ==========================================================
# SSH KEY (HOST SIDE)
# ==========================================================

def ensure_ssh_keys():
    user_cfg = CONFIG["user"]
    key_dir = Path(user_cfg["ssh_key_dir"])
    key_dir.mkdir(parents=True, exist_ok=True)
    priv = key_dir / user_cfg["ssh_key_name"]
    pub = Path(str(priv) + ".pub")

    if not priv.exists():
        run(f"ssh-keygen -t rsa -b 4096 -f {priv} -N ''")
    return priv, pub


# ==========================================================
# START CONTAINER (USED ONLY DURING SETUP)
# ==========================================================

def start_container(node, is_control=False):
    r = runtime()
    net = CONFIG["network"]["name"]
    name = container_name(node)
    role, icon = node_role(node)
    color = UI.CYAN if is_control else UI.YELLOW

    print(f"{color}{icon} {role:<{UI.ROLE_W}} {node['name']:<{UI.NODE_W}} (image: {node['image']}){UI.RESET}")
    port_args, port_info = "", "-"
    if is_control:
        for p in CONFIG["control_node"]["ports"]:
            port_args += f" -p {p['host']}:{p['container']}"
            port_info = f"SSH localhost:{p['host']}"
    volume_arg, volume_info = "", "-"
    if is_control and CONFIG.get("workspace", {}).get("enabled", False):
        ws = CONFIG["workspace"]
        Path(ws["local_base_dir"]).mkdir(parents=True, exist_ok=True)
        volume_arg = f"-v {ws['local_base_dir']}:{ws['container_path']}"
        volume_info = ws["container_path"]

    print(f"   🌐 Network   : {net}")
    print(f"   🚪 Access    : {port_info}")
    print(f"   💾 Workspace : {volume_info}")

    run(
        f"{r} run -d "
        f"--name {name} "
        f"--hostname {node['hostname']} "
        f"--network {net} "
        f"{port_args} "
        f"{volume_arg} "
        f"{node['image']}"
    )
    print(f"{UI.GREEN}   {UI.ICON_OK} {node['name']} started{UI.RESET}\n")


# ==========================================================
# REMOVE / STOP
# ==========================================================

def stop_all():
    r = runtime()
    for node in all_nodes():
        run(f"{r} stop {container_name(node)}", check=False)

def remove_all():
    r = runtime()
    for node in all_nodes():
        run(f"{r} rm -f {container_name(node)}", check=False)


# ==========================================================
# STATUS
# ==========================================================

def status():
    r = runtime()
    net = CONFIG["network"]["name"]

    def container_state(name):
        result = subprocess.run(f"{r} inspect -f '{{{{.State.Status}}}}' {name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        return "unavailable" if result.returncode != 0 else result.stdout.strip()

    def format_state(state):
        return (
            f"{UI.GREEN}🟢 RUNNING{UI.RESET}" if state == "running" else
            f"{UI.YELLOW}🟡 STOPPED{UI.RESET}" if state == "exited" else
            f"{UI.RED}🔴 UNAVAILABLE{UI.RESET}"
        )

    print(f"\n{UI.CYAN}📊 Ansible Lab Status{UI.RESET}")
    print(f"{UI.CYAN}Runtime:{UI.RESET} {r}   {UI.CYAN}Network:{UI.RESET} {net}\n")

    section("CONTROL NODE")
    print(f"{'ROLE':<{UI.ROLE_W}} {'NODE':<{UI.NODE_W}} {'STATUS':<{UI.STAT_W}} ACCESS")
    print("-" * 60)

    ctrl = CONFIG["control_node"]
    cname = container_name(ctrl)
    cstate = container_state(cname)
    access = "-"
    if cstate == "running":
        for p in ctrl.get("ports", []):
            access = f"SSH localhost:{p['host']}"
    role, icon = node_role(ctrl)
    print(f"{icon} {role:<{UI.ROLE_W}} {ctrl['name']:<{UI.NODE_W}} {format_state(cstate):<{UI.STAT_W}} {access}")

    section("MANAGED NODES")
    print(f"{'ROLE':<{UI.ROLE_W}} {'NODE':<{UI.NODE_W}} {'STATUS':<{UI.STAT_W}}")
    print("-" * 60)
    for node in CONFIG["managed_nodes"]:
        state = container_state(container_name(node))
        role, icon = node_role(node)
        print(f"{icon} {role:<{UI.ROLE_W}} {node['name']:<{UI.NODE_W}} {format_state(state):<{UI.STAT_W}}")

    print()


# ==========================================================
# SSH BOOTSTRAP (SETUP ONLY)
# ==========================================================

def setup_ssh_trust():
    r = runtime()
    _, pub = ensure_ssh_keys()
    user = CONFIG["user"]["name"]
    pub_key = pub.read_text().strip()

    for node in CONFIG["managed_nodes"]:
        run(
            f"{r} exec {container_name(node)} bash -lc \""
            f"mkdir -p /home/{user}/.ssh && "
            f"echo '{pub_key}' >> /home/{user}/.ssh/authorized_keys && "
            f"chown -R {user}:{user} /home/{user}/.ssh && "
            f"chmod 700 /home/{user}/.ssh && "
            f"chmod 600 /home/{user}/.ssh/authorized_keys\""
        )

def install_ssh_key_on_control():
    r = runtime()
    user = CONFIG["user"]["name"]
    cname = container_name(CONFIG["control_node"])
    priv, pub = ensure_ssh_keys()

    run(f"{r} exec {cname} mkdir -p /home/{user}/.ssh")
    run(f"{r} cp {priv} {cname}:/home/{user}/.ssh/id_rsa")
    run(f"{r} cp {pub} {cname}:/home/{user}/.ssh/id_rsa.pub")
    run(
        f"{r} exec {cname} bash -lc \""
        f"chown -R {user}:{user} /home/{user}/.ssh && "
        f"chmod 700 /home/{user}/.ssh && "
        f"chmod 600 /home/{user}/.ssh/id_rsa\""
    )

def inject_host_ssh_keys_to_control():
    cfg = CONFIG.get("host_ssh_keys", {})
    if not cfg.get("enabled", False):
        return
    r = runtime()
    user = CONFIG["user"]["name"]
    cname = container_name(CONFIG["control_node"])
    for key_path in cfg["keys"]:
        key_file = Path(key_path).expanduser()
        if not key_file.exists():
            print(f"[WARN] Host SSH key not found: {key_file}")
            continue
        run(
            f"{r} exec {cname} bash -lc \""
            f"mkdir -p /home/{user}/.ssh && "
            f"echo '{key_file.read_text().strip()}' >> /home/{user}/.ssh/authorized_keys && "
            f"chown {user}:{user} /home/{user}/.ssh/authorized_keys && "
            f"chmod 600 /home/{user}/.ssh/authorized_keys\""
        )

def configure_ssh_client_on_control():
    if not CONFIG.get("ssh", {}).get("skip_host_key_check", False):
        return
    r = runtime()
    user = CONFIG["user"]["name"]
    cname = container_name(CONFIG["control_node"])
    ssh_cfg = """Host *
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    GlobalKnownHostsFile /dev/null
    LogLevel ERROR
"""
    run(
        f"{r} exec {cname} bash -lc \""
        f"mkdir -p /home/{user}/.ssh && "
        f"echo '{ssh_cfg}' > /home/{user}/.ssh/config && "
        f"chown {user}:{user} /home/{user}/.ssh/config && "
        f"chmod 600 /home/{user}/.ssh/config\""
    )


# ==========================================================
# ENABLE UX (PS1 + inventory)
# ==========================================================

def create_initial_inventory_on_control():
    r = runtime()
    user = CONFIG["user"]["name"]
    cname = container_name(CONFIG["control_node"])
    hosts = "\n".join(n["name"] for n in CONFIG["managed_nodes"])
    inventory = f"[managed]\n{hosts}\n"
    run(
        f"{r} exec {cname} bash -lc \""
        f"echo '{inventory}' > /home/{user}/inventory.ini && "
        f"chown {user}:{user} /home/{user}/inventory.ini && "
        f"chmod 600 /home/{user}/inventory.ini\""
    )

def configure_bash_prompt():
    r = runtime()
    user = CONFIG["user"]["name"]

    control_ps1 = r'\[\e[1;31m\][\u@\h \W]\$\[\e[0m\] '
    managed_ps1 = r'\[\e[1;32m\][\u@\h \W]\$\[\e[0m\] '

    def apply(cname, ps1):
        run(
            f"""{r} exec {cname} bash -lc "
mkdir -p /home/{user}/.ssh

# Ensure .bash_profile exists and sources .bashrc
if [ ! -f /home/{user}/.bash_profile ]; then
  touch /home/{user}/.bash_profile
fi
grep -q '. ~/.bashrc' /home/{user}/.bash_profile || echo 'if [ -f ~/.bashrc ]; then . ~/.bashrc; fi' >> /home/{user}/.bash_profile

# Write PS1 if missing (tagged)
grep -q 'ANSLAB_PS1' /home/{user}/.bashrc || cat << 'EOF' >> /home/{user}/.bashrc
# ANSLAB_PS1
export PS1='{ps1}'
EOF

# Fix ownership
chown {user}:{user} /home/{user}/.bashrc /home/{user}/.bash_profile
"
"""
        )

    # Apply to control node (red)
    apply(container_name(CONFIG["control_node"]), control_ps1)

    # Apply to managed nodes (green)
    for node in CONFIG["managed_nodes"]:
        apply(container_name(node), managed_ps1)

    print("🎨 Colored bash prompts configured")




# ==========================================================
# COMMAND HANDLERS
# ==========================================================

def cmd_build():
    run("./image_build.py")

def cmd_setup():
    ensure_network()
    start_container(CONFIG["control_node"], is_control=True)
    for n in CONFIG["managed_nodes"]:
        start_container(n)
    install_ssh_key_on_control()
    setup_ssh_trust()
    inject_host_ssh_keys_to_control()
    configure_ssh_client_on_control()
    create_initial_inventory_on_control()
    configure_bash_prompt()

def cmd_start():
    r = runtime()
    section(f"{UI.ICON_RUN} Starting Ansible Lab Containers")
    print(f"{'ROLE':<{UI.ROLE_W}} {'NODE':<{UI.NODE_W}} STATUS")
    print("-" * 60)
    missing = False
    for node in all_nodes():
        role, icon = node_role(node)
        cname = container_name(node)
        print(f"{icon} {role:<{UI.ROLE_W}} {node['name']:<{UI.NODE_W}} ", end="")
        if not container_exists(cname):
            print(f"{UI.RED}NOT CREATED{UI.RESET}")
            missing = True
            continue
        result = subprocess.run(f"{r} start {cname}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{UI.GREEN}STARTED{UI.RESET}" if result.returncode == 0 else f"{UI.YELLOW}ALREADY RUNNING{UI.RESET}")
    if missing:
        print(f"\n{UI.RED}{UI.ICON_ERR} Missing containers – run './ansible_lab.py setup'{UI.RESET}\n")
    else:
        print(f"\n{UI.GREEN}{UI.ICON_OK} Lab started successfully{UI.RESET}\n")

def cmd_stop():
    r = runtime()
    section(f"{UI.ICON_STOP} Stopping Ansible Lab Containers")
    row(f"{'ROLE':<{UI.ROLE_W}}", f"{'NODE':<{UI.NODE_W}}", "STATUS")
    print("-" * 60)
    for node in all_nodes():
        role, icon = node_role(node)
        name = container_name(node)
        print(f"{icon} {role:<{UI.ROLE_W}} {node['name']:<{UI.NODE_W}} ", end="")
        run(f"{r} stop {name}", check=False)
        print(f"{UI.YELLOW}STOPPED{UI.RESET}")
    print(f"\n{UI.YELLOW}{UI.ICON_WARN} Containers stopped (data preserved){UI.RESET}\n")

def cmd_decom():
    r = runtime()
    net = CONFIG["network"]["name"]
    section(f"{UI.ICON_DECOM} Decommissioning Ansible Lab")
    print("🧹 Stopping containers...")
    stop_all()
    print("🗑 Removing containers...")
    remove_all()
    print(f"🌐 Removing network: {net}")
    run(f"{r} network rm {net}", check=False)
    print(f"\n{UI.RED}{UI.ICON_ERR} Lab decommissioned (images & workspace preserved){UI.RESET}\n")

def cmd_status():
    status()

def cmd_info():
    print("\nLab Configuration:\n")
    print(indent(yaml.dump(CONFIG, sort_keys=False), "  "))


# ==========================================================
# MAIN
# ==========================================================

def all_nodes():
    return [CONFIG["control_node"]] + CONFIG["managed_nodes"]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ansible_lab.py {build|setup|start|stop|decom|status|info}")
        sys.exit(1)
    CONFIG = load_config()
    action = sys.argv[1]
    actions = {
        "build": cmd_build,
        "setup": cmd_setup,
        "start": cmd_start,
        "stop": cmd_stop,
        "decom": cmd_decom,
        "status": cmd_status,
        "info": cmd_info,
    }
    if action not in actions:
        print(f"[ERROR] Unknown command: {action}")
        sys.exit(1)
    actions[action]()
