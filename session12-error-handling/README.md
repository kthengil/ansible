# Session 12 – Error Handling and Failure Control

## Why Error Handling Is Required

In real systems:

- commands fail
- packages may already exist or be missing
- services may behave differently
- partial failures are common

A good playbook:

- does not stop unnecessarily
- reacts intelligently to failures
- reports correct status
- cleans up after errors

---

## Default Ansible Behavior on Failure

By default:

- if a task fails
- Ansible **stops executing tasks for that host**
- moves on to the next host

This is safe, but sometimes **too strict**.

---

## `ignore_errors`

Allows playbook execution to continue even if a task fails.

```yaml
ignore_errors: true
```

Example:

```yaml
- name: Try removing a non-existent package
  dnf:
    name: telnet
    state: absent
  ignore_errors: true
```

Use carefully — ignored errors still occurred.

---

## Checking Return Codes (`rc`)

Many modules return a result code.

```yaml
register: result
```

Then inspect:

```yaml
result.rc
```

Common usage:

```yaml
- name: Run command
  command: rpm -q httpd
  register: httpd_check
  ignore_errors: true

- debug:
    var: httpd_check.rc
```

---

## `failed_when`

Control **what Ansible considers a failure**.

```yaml
failed_when: condition
```

Example:

```yaml
- name: Check service status
  command: systemctl status sshd
  register: sshd_status
  failed_when: sshd_status.rc not in [0, 3]
```

This prevents false failures.

---

## `changed_when`

Control **change reporting**.

```yaml
changed_when: false
```

Useful for read-only checks.

Example:

```yaml
- name: Check uptime
  command: uptime
  register: uptime_result
  changed_when: false
```

---

## Combining `failed_when` and `changed_when`

```yaml
- name: Custom command evaluation
  command: some_command
  register: result
  failed_when: result.rc != 0
  changed_when: false
```

This gives full control.

---

## Error Handling with `block`

`block` groups tasks together.

```yaml
block:
  - task1
  - task2
```

If any task inside fails, control can move to `rescue`.

---

## `rescue` – What to Do on Failure

```yaml
rescue:
  - recovery_task
```

Runs only if the block fails.

---

## `always` – Runs No Matter What

```yaml
always:
  - cleanup_task
```

Runs whether block succeeds or fails.

---

## Full Error Handling Example

Create the file:

`error-handling-playbook.yaml`

```yaml
- name: Error handling demonstration
  hosts: all
  become: true

  tasks:
    - name: Application deployment block
      block:
        - name: Create application directory
          file:
            path: /opt/error_demo
            state: directory
            mode: "0755"

        - name: Install non-existent package (intentional failure)
          dnf:
            name: fakepackage
            state: present

      rescue:
        - name: Handle failure gracefully
          debug:
            msg: "Package installation failed, performing recovery steps"

        - name: Create failure marker
          file:
            path: /tmp/deploy_failed.txt
            state: touch

      always:
        - name: Always run cleanup or logging
          debug:
            msg: "Deployment attempt completed"
```

---

## Running the Playbook

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini error-handling-playbook.yaml
```

Observe:

- block fails
- rescue executes
- always executes
- playbook continues cleanly

---

## Error Handling Best Practices

- Use `block/rescue/always` for grouped logic
- Avoid overusing `ignore_errors`
- Always log or mark failures
- Keep recovery actions simple
- Prefer explicit failure logic

---

## Common Mistakes

- Ignoring errors without handling them
- Masking real problems with `ignore_errors`
- Using shell commands without checking rc
- Forgetting `always` for cleanup
- Treating errors as normal flow

---

## Validation Checklist

You should be able to:

- Explain default failure behavior
- Use `ignore_errors` safely
- Control failures using `failed_when`
- Control change reporting using `changed_when`
- Implement block, rescue, and always
- Design resilient playbooks

---
