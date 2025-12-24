# Session 13 – Roles Basics

## Why Roles Exist

As playbooks grow:

- tasks become repetitive
- files become unmanageable
- reuse becomes difficult

Roles solve this by providing:

- standardized directory structure
- reusability
- separation of concerns
- clean, scalable automation

Roles are the **foundation of real-world Ansible projects**.

---

## What Is a Role

A role is a **self-contained unit of automation** that includes:

- tasks
- variables
- handlers
- templates
- files
- defaults

A role can be:

- reused across playbooks
- shared across projects
- version controlled independently

---

## Standard Role Directory Structure

A typical role looks like this:

```text
roles/
└── webserver/
    ├── tasks/
    │   └── main.yaml
    ├── handlers/
    │   └── main.yaml
    ├── templates/
    ├── files/
    ├── vars/
    │   └── main.yaml
    ├── defaults/
    │   └── main.yaml
    └── meta/
        └── main.yaml
```

Only `tasks/main.yaml` is mandatory.

---

## Role Execution Flow

When a role is applied:

1. defaults are loaded
2. vars are loaded
3. tasks are executed
4. handlers are notified
5. templates/files are rendered if used

Variable precedence:

- defaults → vars → playbook vars → extra vars

---

## Role Used in This Session

Role name:

```text
webserver
```

Purpose:

- install httpd
- deploy a simple config
- manage service lifecycle

---

## File: roles/webserver/defaults/main.yaml

Defaults are **low-priority variables**.
Safe to override.

```yaml
web_package: httpd
web_service: httpd
web_root: /var/www/html
```

---

## File: roles/webserver/vars/main.yaml

Vars are **high-priority variables**.
Use sparingly.

```yaml
web_config_file: /etc/httpd/conf.d/ansible.conf
```

---

## File: roles/webserver/tasks/main.yaml

```yaml
- name: Install web server package
  dnf:
    name: "{{ web_package }}"
    state: present

- name: Deploy web server configuration
  copy:
    content: |
      # Managed by Ansible
      ServerName {{ ansible_hostname }}
    dest: "{{ web_config_file }}"
    mode: "0644"
  notify: restart web server

- name: Ensure web service is running
  service:
    name: "{{ web_service }}"
    state: started
    enabled: true
```

---

## File: roles/webserver/handlers/main.yaml

```yaml
- name: restart web server
  service:
    name: "{{ web_service }}"
    state: restarted
```

---

## Using a Role in a Playbook

Roles are applied at the play level.

---

## File: site.yaml

```yaml
- name: Apply webserver role
  hosts: web
  become: true

  roles:
    - webserver
```

---

## Running the Role-Based Playbook

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini site.yaml
```

Observe:

- role tasks run in order
- handler runs only if config changes
- clean and readable output

---

## Overriding Role Variables

Override defaults in the playbook:

```yaml
roles:
  - role: webserver
    vars:
      web_root: /srv/www
```

Or via command line:

```bash
-e "web_package=httpd"
```

---

## Roles vs Playbooks

| Playbook         | Role           |
| ---------------- | -------------- |
| Orchestration    | Implementation |
| Defines _what_   | Defines _how_  |
| Project-specific | Reusable       |
| Entry point      | Building block |

---

## Common Mistakes

- Putting logic directly in playbooks
- Overusing vars instead of defaults
- Hardcoding values in tasks
- Not using handlers inside roles
- Making roles too generic or too specific

---

## Validation Checklist

You should be able to:

- Explain what a role is
- Describe role directory structure
- Use defaults and vars correctly
- Apply a role in a playbook
- Override role variables safely
- Understand role execution flow

---
