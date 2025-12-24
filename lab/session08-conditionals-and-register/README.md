# Session 08 – Conditionals and Register

---

## Why Conditionals Are Needed

Not all systems should behave the same way.

Conditionals allow tasks to:

- run only when certain conditions are met
- react to system state
- make decisions based on facts or command output

Without conditionals, playbooks are rigid and unsafe.

---

## The `when` Keyword

Conditionals in Ansible are implemented using `when`.

Basic syntax:

```yaml
when: condition
```

The condition must evaluate to **true or false**.

---

## Simple Conditional Example

```yaml
- name: Run only on flame
  command: hostname
  when: ansible_hostname == "flame"
```

The task runs only on the matching host.

---

## Using Facts in Conditions

Facts are commonly used in conditionals.

```yaml
- name: Run on RedHat family systems
  command: cat /etc/redhat-release
  when: ansible_os_family == "RedHat"
```

---

## Multiple Conditions

Use logical operators:

```yaml
when:
  - ansible_os_family == "RedHat"
  - ansible_distribution_major_version | int >= 8
```

All conditions must be true.

---

## OR Conditions

```yaml
when: ansible_hostname == "flame" or ansible_hostname == "frost"
```

---

## Using `register`

`register` captures the output of a task into a variable.

```yaml
- name: Check uptime
  command: uptime
  register: uptime_result
```

The output is stored as a dictionary.

---

## Inspecting Registered Output

```yaml
- name: Show uptime output
  debug:
    var: uptime_result
```

Common fields:

- `stdout`
- `stderr`
- `rc` (return code)
- `changed`

---

## Using Registered Output in Conditions

```yaml
- name: Create marker file if system is up
  file:
    path: /tmp/system_up.txt
    state: touch
  when: uptime_result.rc == 0
```

---

## Practical Example – Command Check + Conditional Action

```yaml
- name: Check if httpd is installed
  command: rpm -q httpd
  register: httpd_check
  ignore_errors: true

- name: Install httpd if missing
  dnf:
    name: httpd
    state: present
  when: httpd_check.rc != 0
```

---

## `ignore_errors` vs `failed_when`

### ignore_errors

Allows playbook to continue after failure.

```yaml
ignore_errors: true
```

### failed_when

Controls what is considered a failure.

```yaml
failed_when: "'not found' in command_result.stderr"
```

---

## Using `changed_when`

Manually control change reporting.

```yaml
changed_when: false
```

Useful for read-only commands.

---

## Conditional Based on File Existence

```yaml
- name: Check if config exists
  stat:
    path: /etc/ssh/sshd_config
  register: sshd_conf

- name: Backup config if present
  copy:
    src: /etc/ssh/sshd_config
    dest: /etc/ssh/sshd_config.bak
    remote_src: true
  when: sshd_conf.stat.exists
```

---

## Full Playbook Example (session08)

Create the file:

`conditional-playbook.yaml`

```yaml
- name: Conditionals and register demo
  hosts: all
  become: true

  tasks:
    - name: Check uptime
      command: uptime
      register: uptime_result
      changed_when: false

    - name: Show uptime
      debug:
        msg: "Uptime: {{ uptime_result.stdout }}"

    - name: Create uptime marker file
      file:
        path: /tmp/uptime_checked.txt
        state: touch
      when: uptime_result.rc == 0

    - name: Check if httpd is installed
      command: rpm -q httpd
      register: httpd_check
      ignore_errors: true
      changed_when: false

    - name: Install httpd if not installed
      dnf:
        name: httpd
        state: present
      when: httpd_check.rc != 0
```

---

## Running the Playbook

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini conditional-playbook.yaml
```

---

## Common Mistakes

- Using `=` instead of `==` in conditions
- Forgetting that `when` does not use `{{ }}`
- Not checking return codes (`rc`)
- Using `ignore_errors` without understanding consequences
- Assuming registered variables are strings (they are dictionaries)

---

## Validation Checklist

You should be able to:

- Use `when` with facts
- Register command output
- Inspect registered variables
- Make decisions based on command results
- Control failure and change behavior
- Combine multiple conditions safely

---
