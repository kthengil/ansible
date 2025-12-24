# Session 06 – Modules Deep Dive

---

## What a Module Is

A module is the **actual unit of work** in Ansible.

When you run a task, Ansible:

- copies the module to the managed node
- executes it using Python
- removes it after execution
- returns structured output

Every task uses **exactly one module**.

---

## Why Modules Matter

Modules provide:

- idempotency
- predictable behavior
- structured input and output
- safety compared to raw commands

Using the correct module is the **most important Ansible skill**.

---

## Module vs Command vs Shell

### command module

- Executes commands directly
- No shell features
- Safer
- Preferred when possible

### shell module

- Executes via shell
- Supports pipes, redirects, variables
- Higher risk
- Use only when required

### specialized modules

- dnf, service, copy, file, user, template, etc.
- Built for specific tasks
- Idempotent by design

---

## General Task Structure with Modules

```yaml
- name: Task description
  module_name:
    option1: value
    option2: value
```

Avoid using:

```yaml
- shell: yum install httpd
```

Prefer:

```yaml
- dnf:
    name: httpd
    state: present
```

---

## Package Management – dnf Module

### Install a package

```yaml
- name: Install vim
  dnf:
    name: vim
    state: present
```

### Install multiple packages

```yaml
- name: Install common tools
  dnf:
    name:
      - vim
      - git
      - curl
    state: present
```

### Remove a package

```yaml
- name: Remove vim
  dnf:
    name: vim
    state: absent
```

---

## Service Management – service Module

### Start a service

```yaml
- name: Start sshd
  service:
    name: sshd
    state: started
```

### Enable a service at boot

```yaml
- name: Enable sshd
  service:
    name: sshd
    enabled: true
```

### Restart a service

```yaml
- name: Restart sshd
  service:
    name: sshd
    state: restarted
```

---

## File Management – file Module

### Create a directory

```yaml
- name: Create application directory
  file:
    path: /opt/app
    state: directory
    owner: root
    group: root
    mode: "0755"
```

### Remove a file or directory

```yaml
- name: Remove directory
  file:
    path: /opt/app
    state: absent
```

---

## Copying Files – copy Module

### Copy content directly

```yaml
- name: Create a test file
  copy:
    content: "Managed by Ansible\n"
    dest: /tmp/ansible-test.txt
    mode: "0644"
```

### Copy a file from control node

```yaml
- name: Copy config file
  copy:
    src: files/app.conf
    dest: /etc/app.conf
    owner: root
    group: root
    mode: "0644"
```

---

## Command Execution – command Module

### Run a command

```yaml
- name: Check hostname
  command: hostname
```

### Capture output (preview)

```yaml
- name: Check uptime
  command: uptime
  register: uptime_output
```

Output handling is covered in later sessions.

---

## Shell Execution – shell Module

### Use shell features

```yaml
- name: Disk usage check
  shell: df -h | grep /
```

Use shell only when:

- pipes are needed
- redirects are needed
- environment variables are required

---

## Understanding Idempotency

Idempotent task:

- Can run multiple times
- Produces same result
- Does not repeat changes unnecessarily

Example:

```yaml
- dnf:
    name: httpd
    state: present
```

Non-idempotent example:

```yaml
- shell: echo hello >> /tmp/file
```

---

## Reading Module Documentation

Use built-in documentation:

```bash
ansible-doc dnf
ansible-doc service
ansible-doc copy
ansible-doc file
```

Search for modules:

```bash
ansible-doc -l | grep user
```

---

## Choosing the Right Module – Mental Checklist

Ask yourself:

1. Is there a dedicated module for this task?
2. Is it idempotent?
3. Does it require root privileges?
4. Can I avoid shell?
5. Is the module OS-specific?

---

## Common Beginner Mistakes

- Using shell for everything
- Ignoring module documentation
- Assuming modules behave like shell commands
- Forgetting required arguments
- Mixing module syntax styles incorrectly

---

## Validation Checklist

You should be able to:

- Explain what a module is
- Choose the correct module for a task
- Use dnf, service, file, copy correctly
- Avoid unnecessary shell usage
- Read and understand module documentation
- Identify idempotent vs non-idempotent tasks

---
