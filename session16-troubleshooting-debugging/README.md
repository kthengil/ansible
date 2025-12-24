# Session 16 – Troubleshooting and Debugging

---

## Why Troubleshooting Skills Matter

In real environments:

- automation will fail
- systems will behave differently
- permissions will break
- inventories will be wrong

Strong troubleshooting skills allow you to:

- identify root causes quickly
- fix issues safely
- avoid blind retries
- gain confidence in automation

---

## Default Failure Behavior Recap

- Task fails → host execution stops
- Other hosts continue
- Failure message is shown
- Playbook exits with non-zero status

Understanding this behavior is critical for debugging.

---

## Increasing Verbosity

Ansible provides multiple verbosity levels.

```bash
-v     # basic task execution info
-vv    # connection and SSH details
-vvv   # full debug including module execution
-vvvv  # extremely verbose (rarely needed)
```

Example:

```bash
ansible-playbook -i inventory.ini playbook.yaml -vvv
```

---

## Most Common Failure Categories

- SSH connectivity issues
- Authentication / sudo failures
- Inventory parsing errors
- YAML syntax errors
- Module argument errors
- Permission denied issues

---

## SSH and Connectivity Issues

### Symptoms

- UNREACHABLE errors
- Permission denied
- Timeout

### Checks

```bash
ssh flame
```

```bash
ansible -i inventory.ini all -m ping -vv
```

Verify:

- SSH key access
- correct user
- network reachability

---

## Inventory Issues

### Common Problems

- wrong inventory file used
- hostnames not resolvable
- group name typos

### Debug Commands

```bash
ansible-inventory -i inventory.ini --list
```

```bash
ansible-inventory -i inventory.ini --graph
```

---

## YAML Syntax Errors

YAML errors are **parse-time failures**.

Symptoms:

- unexpected indent
- mapping values are not allowed
- could not find expected ':'

Fix strategy:

- check indentation
- verify lists vs dictionaries
- remove tabs
- simplify and retry

---

## Module Argument Errors

Example:

```yaml
service:
  name: sshd
  started: true # invalid argument
```

Error messages usually explain the issue.

Check module docs:

```bash
ansible-doc service
```

---

## Using the `debug` Module

Print variables:

```yaml
- debug:
    var: ansible_hostname
```

Print messages:

```yaml
- debug:
    msg: "Value of port is {{ app_port }}"
```

Use debug **liberally while developing**.

---

## Register + Debug Pattern

```yaml
- name: Run command
  command: uptime
  register: uptime_result

- debug:
    var: uptime_result
```

This exposes:

- stdout
- stderr
- rc
- changed

---

## Checking Facts During Debugging

```bash
ansible -i inventory.ini all -m setup | less
```

Filter facts:

```bash
ansible -i inventory.ini all -m setup -a "filter=ansible_*_version"
```

---

## Privilege Escalation Issues

Symptoms:

- permission denied
- sudo required

Fix:

- add `become: true`
- verify sudo access for user

Test:

```bash
ansible -i inventory.ini all -m command -a "whoami" -b
```

---

## Testing with `--check`

Dry-run helps identify logic errors.

```bash
ansible-playbook -i inventory.ini playbook.yaml --check
```

Combine with diff:

```bash
--check --diff
```

---

## Isolating Failures

Limit execution:

```bash
--limit flame
```

Run a single task with tags (preview):

```bash
--tags install
```

---

## Debugging Playbook Structure

Break large playbooks:

- comment out sections
- run incrementally
- validate after each change

---

## Reading Error Output Correctly

Focus on:

- **first error**, not the last
- module name
- argument shown
- file and line number

Most failures are **simple misconfigurations**.

---

## Common Mistakes

- Skipping verbosity
- Ignoring error messages
- Guessing instead of validating
- Overusing ignore_errors
- Debugging all hosts at once

---

## Troubleshooting Mindset

1. Reproduce the problem
2. Reduce scope
3. Increase verbosity
4. Inspect variables and facts
5. Fix root cause
6. Re-run cleanly

---

## 📄 `debug-playbook.yaml`

```yaml
- name: Debugging and troubleshooting demonstration
  hosts: all
  become: true

  tasks:
    - name: Print basic host information
      debug:
        msg:
          - "Hostname: {{ ansible_hostname }}"
          - "OS Family: {{ ansible_os_family }}"
          - "OS Version: {{ ansible_distribution }} {{ ansible_distribution_major_version }}"

    - name: Check uptime
      command: uptime
      register: uptime_result
      changed_when: false

    - name: Debug uptime command output
      debug:
        var: uptime_result

    - name: Verify SSH service status
      command: systemctl is-active sshd
      register: sshd_status
      ignore_errors: true
      changed_when: false

    - name: Debug SSH service status
      debug:
        msg: "SSHD service state: {{ sshd_status.stdout | default('unknown') }}"

    - name: Check disk usage
      shell: df -h /
      register: disk_usage
      changed_when: false

    - name: Debug disk usage output
      debug:
        msg: "{{ disk_usage.stdout_lines }}"

    - name: Conditional debug if disk usage is high
      debug:
        msg: "Warning: Disk usage might be high"
      when: disk_usage.stdout is search('9[0-9]%')
```

---

## ▶️ How to Run This Debug Playbook

From the session directory:

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini debug-playbook.yaml
```

Increase verbosity for deeper insight:

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini debug-playbook.yaml -vvv
```

---

## 🎯 What This Playbook Demonstrates

- `debug` with `msg` and `var`
- inspecting registered variables
- handling command failures safely
- using `changed_when` for read-only tasks
- conditional debugging
- structured output for troubleshooting

---

## ✅ After Running, You Should Understand

- how to inspect task output safely
- how to debug variables and facts
- how to detect potential issues without failing the play
- how verbosity changes execution visibility

---

## Validation Checklist

You should be able to:

- Use verbosity effectively
- Diagnose SSH and inventory issues
- Debug YAML and module errors
- Inspect variables and facts
- Isolate and fix failures
- Apply systematic troubleshooting

---
