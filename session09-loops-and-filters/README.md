# Session 09 – Loops and Filters

## Why Loops Are Needed

Without loops:

- tasks get duplicated
- playbooks become long and hard to maintain
- small changes require multiple edits

Loops allow:

- iterating over lists
- iterating over dictionaries
- performing the same task on multiple items
- cleaner and scalable playbooks

---

## The `loop` Keyword

Modern Ansible uses `loop`.

Basic syntax:

```yaml
loop:
  - item1
  - item2
  - item3
```

Each iteration exposes the variable `item`.

---

## Simple Loop Example

```yaml
- name: Install multiple packages
  dnf:
    name: "{{ item }}"
    state: present
  loop:
    - vim
    - git
    - curl
```

The task runs once per item.

---

## Loop with Variables

```yaml
packages:
  - vim
  - git
  - curl
```

```yaml
- name: Install packages
  dnf:
    name: "{{ item }}"
    state: present
  loop: "{{ packages }}"
```

---

## Looping Over Files

```yaml
- name: Create multiple directories
  file:
    path: "/opt/{{ item }}"
    state: directory
  loop:
    - app1
    - app2
    - app3
```

---

## Looping Over Dictionaries

Use `dict2items` filter.

```yaml
users:
  alice: 1001
  bob: 1002
```

```yaml
- name: Show user data
  debug:
    msg: "User {{ item.key }} has UID {{ item.value }}"
  loop: "{{ users | dict2items }}"
```

---

## Loop Control

### Custom loop variable

```yaml
loop_control:
  loop_var: pkg
```

```yaml
- name: Install packages
  dnf:
    name: "{{ pkg }}"
    state: present
  loop: "{{ packages }}"
  loop_control:
    loop_var: pkg
```

---

## Loop Index

```yaml
loop_control:
  index_var: index
```

```yaml
- debug:
    msg: "Item {{ index }} is {{ item }}"
  loop:
    - one
    - two
    - three
```

---

## Conditional Loops

Combine `loop` with `when`.

```yaml
- name: Install only on RedHat systems
  dnf:
    name: "{{ item }}"
    state: present
  loop:
    - vim
    - git
  when: ansible_os_family == "RedHat"
```

---

## Loop with Register

Register captures results for all iterations.

```yaml
- name: Check files
  stat:
    path: "/tmp/{{ item }}"
  loop:
    - a.txt
    - b.txt
  register: file_checks
```

Result structure:

- `file_checks.results` (list)

---

## Using Registered Loop Results

```yaml
- debug:
    msg: "{{ item.stat.exists }}"
  loop: "{{ file_checks.results }}"
```

---

## Filters – Why They Matter

Filters transform data.

Used to:

- convert types
- extract values
- manipulate strings
- control data format

Filters are part of **Jinja2**.

---

## Commonly Used Filters

### `length`

```yaml
{ { packages | length } }
```

---

### `default`

```yaml
{ { app_port | default(8080) } }
```

---

### `upper` and `lower`

```yaml
{{ app_name | upper }}
{{ app_name | lower }}
```

---

### `join`

```yaml
{{ packages | join(', ') }}
```

---

### `int`

```yaml
{ { ansible_distribution_major_version | int } }
```

---

## Practical Example – Loop + Filter

```yaml
- name: Create files with uppercase names
  file:
    path: "/tmp/{{ item | upper }}"
    state: touch
  loop:
    - one
    - two
    - three
```

---

## Full Playbook Example (session09)

Create the file:

`loop-playbook.yaml`

```yaml
- name: Loop and filter demonstration
  hosts: all
  become: true

  vars:
    packages:
      - vim
      - git
      - curl

    app_dirs:
      - app1
      - app2
      - app3

  tasks:
    - name: Install multiple packages
      dnf:
        name: "{{ item }}"
        state: present
      loop: "{{ packages }}"

    - name: Create application directories
      file:
        path: "/opt/{{ item }}"
        state: directory
        mode: "0755"
      loop: "{{ app_dirs }}"

    - name: Create uppercase marker files
      file:
        path: "/tmp/{{ item | upper }}.txt"
        state: touch
      loop: "{{ app_dirs }}"

    - name: Show installed package count
      debug:
        msg: "Total packages: {{ packages | length }}"
```

---

## Running the Playbook

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini loop-playbook.yaml
```

---

## Common Mistakes

- Using deprecated `with_items`
- Forgetting `item` variable
- Incorrect indentation under `loop`
- Misunderstanding `results` when registering loops
- Overusing loops when a module supports lists natively

---

## Validation Checklist

You should be able to:

- Use `loop` correctly
- Loop over lists and dictionaries
- Combine loops with conditionals
- Use filters to transform data
- Register loop results and inspect them
- Reduce repetitive tasks effectively

---
