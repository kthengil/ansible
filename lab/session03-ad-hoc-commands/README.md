# Session 03 – Ad-hoc Commands

---

## Objective

This session focuses on using Ansible **without playbooks** by executing ad-hoc commands.

By the end of this session, you will:

- Understand what ad-hoc commands are
- Learn the structure of an Ansible ad-hoc command
- Use commonly required modules
- Perform real administrative tasks across multiple nodes
- Understand idempotency at the module level

---

## What Are Ad-hoc Commands?

Ad-hoc commands are **one-line Ansible executions** used for:

- Quick checks
- One-time tasks
- Troubleshooting
- Learning module behavior

They are **imperative**, not declarative.

Ad-hoc commands do **not** replace playbooks, but complement them.

---

## General Syntax

```bash
ansible <host-pattern> -i <inventory> -m <module> -a "<arguments>"
```

Key components:

- `host-pattern` → which hosts to target
- `-i` → inventory file
- `-m` → module name
- `-a` → module arguments

---

## Inventory Used in This Session

We will reuse the inventory created in Session 02.

```bash
inventory.ini
```

Hosts:

- flame
- frost
- storm
- earth
- water

---

## Connectivity Check (Baseline)

```bash
ansible -i inventory.ini all -m ping
```

Purpose:

- Validate SSH connectivity
- Validate Python availability
- Confirm inventory correctness

---

## Using the `command` Module

The `command` module:

- Executes commands directly
- Does NOT support shell features like pipes or redirects
- Is safer and preferred over `shell`

### Example: Check hostname

```bash
ansible -i inventory.ini all -m command -a "hostname"
```

---

### Example: Check OS release

```bash
ansible -i inventory.ini all -m command -a "cat /etc/os-release"
```

---

## Using the `shell` Module

The `shell` module:

- Executes through a shell
- Supports pipes, redirects, variables
- Should be used only when required

### Example: Use pipes

```bash
ansible -i inventory.ini all -m shell -a "df -h | grep /"
```

---

### Example: Redirect output

```bash
ansible -i inventory.ini all -m shell -a "uptime > /tmp/uptime.txt"
```

---

## Difference: command vs shell

| command           | shell                |
| ----------------- | -------------------- |
| Safer             | Less safe            |
| No shell features | Full shell support   |
| Preferred         | Use only when needed |

---

## Gathering System Facts (Preview)

```bash
ansible -i inventory.ini all -m setup
```

To filter specific facts:

```bash
ansible -i inventory.ini all -m setup -a "filter=ansible_hostname"
```

Facts will be heavily used in later sessions.

---

## Package Management Using `dnf`

Install a package across all hosts:

```bash
ansible -i inventory.ini all -m dnf -a "name=vim state=present" -b
```

Key points:

- `-b` enables privilege escalation
- `dnf` module is idempotent
- Safe to run multiple times

---

Remove a package:

```bash
ansible -i inventory.ini all -m dnf -a "name=vim state=absent" -b
```

---

## Service Management Using `service`

Start a service:

```bash
ansible -i inventory.ini all -m service -a "name=sshd state=started" -b
```

Enable a service:

```bash
ansible -i inventory.ini all -m service -a "name=sshd enabled=yes" -b
```

Restart a service:

```bash
ansible -i inventory.ini all -m service -a "name=sshd state=restarted" -b
```

---

## File Management Using `copy`

Create a file on all nodes:

```bash
ansible -i inventory.ini all -m copy -a "content='Managed by Ansible\n' dest=/tmp/ansible-test.txt" -b
```

Verify file:

```bash
ansible -i inventory.ini all -m command -a "cat /tmp/ansible-test.txt"
```

---

## Directory Management Using `file`

Create a directory:

```bash
ansible -i inventory.ini all -m file -a "path=/opt/app state=directory mode=0755" -b
```

Remove a directory:

```bash
ansible -i inventory.ini all -m file -a "path=/opt/app state=absent" -b
```

---

## Understanding Idempotency

Run this command multiple times:

```bash
ansible -i inventory.ini all -m dnf -a "name=httpd state=present" -b
```

Observation:

- First run → changes occur
- Subsequent runs → no changes

This is **idempotency**.

---

## Targeting Specific Hosts and Groups

Single host:

```bash
ansible -i inventory.ini flame -m command -a "hostname"
```

Group:

```bash
ansible -i inventory.ini web -m command -a "hostname"
```

Multiple groups:

```bash
ansible -i inventory.ini web:db -m command -a "hostname"
```

---

## Limiting Scope

Limit execution:

```bash
ansible -i inventory.ini all -m command -a "hostname" --limit flame
```

---

## Verbosity for Debugging

Increase verbosity:

```bash
ansible -i inventory.ini all -m ping -v
ansible -i inventory.ini all -m ping -vv
ansible -i inventory.ini all -m ping -vvv
```

---

## Common Mistakes

- Using `shell` unnecessarily
- Forgetting `-b` for privileged tasks
- Assuming ad-hoc commands replace playbooks
- Running destructive commands without `--limit`

---

## Validation Checklist

You should be able to:

- Run ad-hoc commands on all nodes
- Use `command` and `shell` appropriately
- Install and remove packages
- Manage services
- Create and remove files/directories
- Understand idempotency

---
