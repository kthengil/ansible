# Session 01 – Ansible Basics & First Contact

---

## Objective

This session establishes a strong foundation by validating the Ansible setup, understanding how Ansible works internally, and running the very first commands against managed nodes.

By the end of this session, you will be comfortable with:

- What Ansible is and how it operates
- Core components of Ansible
- Verifying installation
- Running basic Ansible commands
- Understanding inventory and connectivity

---

## Lab Context

**Control Node**

- Hostname: `alpha`

**Managed Nodes**

- `flame`
- `frost`
- `storm`
- `earth`
- `water`

**User**

- `sysansible`

**Assumptions**

- SSH key-based authentication is already configured from `alpha` to all managed nodes
- Ansible is installed on the control node
- Managed nodes do not require Ansible installation

---

## What is Ansible?

Ansible is an **agentless automation tool** used for:

- Configuration management
- Application deployment
- Infrastructure automation
- Orchestration

Key characteristics:

- Uses **SSH** for communication
- Uses **YAML** for playbooks
- Follows a **push-based** model
- Emphasizes **idempotency**

---

## Core Ansible Components

### Control Node

The machine where:

- Ansible is installed
- Commands and playbooks are executed

In this lab:

- `alpha`

---

### Managed Nodes

The machines that Ansible manages.

In this lab:

- `flame`, `frost`, `storm`, `earth`, `water`

---

### Inventory

The inventory defines:

- Which hosts Ansible manages
- How they are grouped
- Connection-related variables

Inventory can be:

- Static (INI / YAML)
- Dynamic (scripts, plugins)

---

### Modules

Modules are the **units of work** in Ansible.

Examples:

- `ping`
- `command`
- `shell`
- `dnf`
- `service`
- `copy`

Ansible executes **one module per task**.

---

### Playbooks

Playbooks are YAML files that define:

- Which hosts to target
- What tasks to execute
- In what order

Playbooks will be covered in later sessions.

---

## Verifying Ansible Installation

Run the following command on the control node (`alpha`):

```bash
ansible --version
```

Expected observations:

- Ansible version is displayed
- Python version used by Ansible
- Configuration file path
- Module search paths

This confirms Ansible is properly installed.

---

## Understanding the Ansible Command Structure

Basic format:

```bash
ansible <host-pattern> -m <module> -a "<arguments>"
```

Where:

- `<host-pattern>` → which hosts to target
- `-m` → module name
- `-a` → module arguments

---

## First Contact: Localhost Test

Test Ansible against the local machine:

```bash
ansible localhost -m ping
```

What happens:

- Ansible runs the `ping` module
- No ICMP ping is used
- Python is executed remotely
- A `pong` response confirms success

---

## Understanding the `ping` Module

The `ping` module:

- Tests connectivity
- Validates Python availability
- Confirms authentication

It does **not** test network latency.

---

## Running Ansible Against Managed Nodes

### Default Inventory Test

Run:

```bash
ansible all -m ping
```

Expected result:

- All managed nodes respond with `pong`
- Confirms:

  - Inventory resolution
  - SSH connectivity
  - User permissions

---

## Listing Hosts Ansible Knows About

```bash
ansible all --list-hosts
```

This command:

- Shows which hosts match the pattern
- Helps debug inventory issues

---

## Checking Facts Availability (Preview)

Run:

```bash
ansible flame -m setup | head
```

What this does:

- Collects system facts
- Displays hardware, OS, network details
- Uses the `setup` module

Facts will be used extensively later.

---

## Testing Commands on Managed Nodes

Run a simple command:

```bash
ansible all -m command -a "hostname"
```

Expected output:

- Each host returns its hostname
- Confirms remote command execution

---

## Important Concepts Introduced

- Agentless architecture
- Push-based execution
- Inventory-driven targeting
- Modules as execution units
- SSH-based communication

---

## Common Mistakes at This Stage

- Assuming Ansible must be installed on managed nodes
- Confusing `ping` with network ping
- Forgetting inventory configuration
- SSH key permission issues

---

## Validation Checklist

You should be able to:

- Run `ansible --version`
- Ping localhost using Ansible
- Ping all managed nodes
- Execute a command remotely
- Understand Ansible’s basic architecture

---
