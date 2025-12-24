# Session 07 – Variables and Facts

---

## Why Variables Matter

Variables make Ansible **dynamic and reusable**.

Without variables:

- playbooks are hard-coded
- reuse is limited
- scaling becomes difficult

With variables:

- one playbook works for many hosts
- behavior changes based on input
- logic becomes flexible

---

## What Are Variables

A variable is a **named value** used in playbooks.

Examples:

- package names
- file paths
- service names
- environment-specific values

Variables are referenced using **Jinja2 syntax**:

```yaml
{ { variable_name } }
```

---

## Variable Naming Rules

- Use lowercase
- Use underscores
- Avoid special characters
- Avoid reserved words

Good:

```yaml
app_name
http_port
service_state
```

Bad:

```yaml
AppName
http-port
1st_var
```

---

## Variable Precedence (High Level)

Variables can come from many places.

Common sources (simplified order):

- command-line variables (`-e`)
- playbook variables
- vars files
- inventory variables
- facts

Higher precedence overrides lower precedence.

---

## File: vars.yaml

This file contains reusable variables.

```yaml
app_name: demo_app
app_dir: /opt/demo_app
app_user: root
app_group: root

packages:
  - vim
  - git
  - curl

service_name: sshd
service_enabled: true
```

---

## File: vars-playbook.yaml

This playbook demonstrates how variables are used.

```yaml
- name: Using variables in a playbook
  hosts: all
  become: true
  vars_files:
    - vars.yaml

  tasks:
    - name: Install packages using variable list
      dnf:
        name: "{{ packages }}"
        state: present

    - name: Create application directory using variables
      file:
        path: "{{ app_dir }}"
        state: directory
        owner: "{{ app_user }}"
        group: "{{ app_group }}"
        mode: "0755"

    - name: Create application info file
      copy:
        content: |
          Application: {{ app_name }}
          Managed by Ansible
        dest: "{{ app_dir }}/info.txt"
        owner: "{{ app_user }}"
        group: "{{ app_group }}"
        mode: "0644"

    - name: Ensure service state using variables
      service:
        name: "{{ service_name }}"
        state: started
        enabled: "{{ service_enabled }}"
```

---

## Running the Playbook

From the session directory:

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini vars-playbook.yaml
```

---

## Overriding Variables at Runtime

Variables can be overridden using `-e`.

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini \
vars-playbook.yaml \
-e "app_name=custom_app app_dir=/opt/custom_app"
```

Command-line variables have **highest precedence**.

---

## Understanding Facts

Facts are **automatically collected variables** about a host.

Examples:

- OS name
- IP address
- CPU count
- Memory
- Hostname

Facts are stored in:

```yaml
ansible_facts
```

---

## Viewing Facts

```bash
ansible -i ../session05-first-playbook/inventory.ini all -m setup
```

Filter specific facts:

```bash
ansible -i ../session05-first-playbook/inventory.ini all -m setup -a "filter=ansible_hostname"
```

---

## Using Facts in Playbooks

Example:

```yaml
- name: Create file with hostname
  copy:
    content: "Hostname: {{ ansible_hostname }}\n"
    dest: /tmp/hostname.txt
```

Facts behave like normal variables.

---

## Disabling Fact Gathering

Fact gathering takes time.

Disable if not needed:

```yaml
- hosts: all
  gather_facts: false
```

Enable only when required.

---

## Variable Debugging

Use the `debug` module:

```yaml
- name: Print variable value
  debug:
    var: app_name
```

Or:

```yaml
- debug:
    msg: "Application directory is {{ app_dir }}"
```

---

## Common Variable Mistakes

- Forgetting `{{ }}` when referencing
- Misspelled variable names
- Assuming variable exists without defining it
- Mixing strings and numbers unintentionally
- Overriding variables unknowingly

---

## Validation Checklist

You should be able to:

- Define variables in a vars file
- Use variables in tasks
- Override variables at runtime
- Explain variable precedence
- Use system facts
- Debug variable values

---
