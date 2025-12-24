# **`Ansible Lab`**

# Ansible Hands-On Practice Lab

---

## Purpose of This Lab

This lab is a **progressive, hands-on Ansible learning environment** designed to move from fundamentals to real-world automation patterns.

The lab is structured into **independent sessions**, each building on previous concepts while remaining self-contained.
Every session can be practiced, repeated, and expanded without affecting others.

---

## Lab Environment Overview

### Control Node

- **Hostname:** `alpha`
- **OS:** UBI 8
- **Ansible:** Installed
- **User:** `sysansible`

### Managed Nodes

- `flame`
- `frost`
- `storm`
- `earth`
- `water`

### Connectivity

- SSH key-based authentication configured
- Passwordless access from control node to all managed nodes
- Privilege escalation available via `become`

---

## Directory Structure

```text
/home/sysansible/lab/
├── README.md
├── session01-ansible-basics
├── session02-inventory-fundamentals
├── session03-ad-hoc-commands
├── session04-yaml-basics-for-ansible
├── session05-first-playbook
├── session06-modules-deep-dive
├── session07-variables-and-facts
├── session08-conditionals-and-register
├── session09-loops-and-filters
├── session10-templates-jinja2
├── session11-handlers-and-notify
├── session12-error-handling
├── session13-roles-basics
├── session14-includes-imports
├── session15-vault-basics
├── session16-troubleshooting-debugging
└── session17-capstone-project
```

---

## Session Design Philosophy

Each session directory contains:

- `README.md`

  - Concept explanation
  - Practical examples
  - Execution guidance

- Supporting files

  - Playbooks (`.yaml`)
  - Inventory files
  - Variable files
  - Templates
  - Role structures

Sessions are:

- Ordered logically
- Focused on one core topic
- Designed for repetition and experimentation
- Written as self-reference notes

---

## Learning Progression

| Session | Focus Area                    |
| ------- | ----------------------------- |
| 01      | Ansible basics & architecture |
| 02      | Inventory design (INI & YAML) |
| 03      | Ad-hoc commands & modules     |
| 04      | YAML fundamentals             |
| 05      | First playbook                |
| 06      | Core modules deep dive        |
| 07      | Variables & facts             |
| 08      | Conditionals & register       |
| 09      | Loops & filters               |
| 10      | Templates & Jinja2            |
| 11      | Handlers & notify             |
| 12      | Error handling                |
| 13      | Roles                         |
| 14      | Includes & imports            |
| 15      | Ansible Vault                 |
| 16      | Troubleshooting & debugging   |
| 17      | Capstone project              |

---

## How to Use This Lab

### Recommended Workflow

1. Start with **Session 01**
2. Read the `README.md`
3. Run commands and playbooks
4. Modify examples
5. Re-run to observe idempotency
6. Move to the next session

Avoid skipping sessions unless already comfortable with the topic.

---

## Inventory Usage

Most sessions reuse the inventory created in **Session 05**.

Example usage pattern:

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini playbook.yaml
```

This keeps inventory management consistent across sessions.

---

## Best Practices Followed

- No hard-coded credentials
- Minimal shell usage
- Idempotent modules preferred
- Clean separation of logic
- Enterprise-style structure
- Debug-first mindset
- Safe error handling

---

## Expectations From the Learner

By completing this lab, you should be able to:

- Design clean Ansible playbooks
- Debug failures confidently
- Structure automation using roles
- Secure secrets using Vault
- Apply Ansible to real systems safely
- Understand _why_ something works, not just _how_

---

## Capstone Session

The final session brings together:

- inventory
- variables
- templates
- handlers
- roles
- conditionals
- error handling

It represents a **real-world automation scenario**, not a demo.

---
