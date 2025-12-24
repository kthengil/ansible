# Session 11 – Handlers and Notify

## Why Handlers Exist

Some actions should run **only when something changes**.

Examples:

- restart a service only if config changed
- reload a daemon only after file update
- avoid unnecessary restarts

Handlers solve this by being **event-driven**.

---

## What Is a Handler

A handler is a **special task** that:

- runs only when notified
- runs at the end of a play
- runs once even if notified multiple times

Handlers use the same modules as normal tasks.

---

## The `notify` Mechanism

A task can trigger a handler using `notify`.

```yaml
notify: handler_name
```

The handler executes only if the task reports `changed`.

---

## Handler Execution Behavior

- Runs after all tasks in the play finish
- Runs once per handler name
- Multiple notifications → single execution
- Order is preserved

---

## Basic Handler Example

```yaml
tasks:
  - name: Update configuration
    template:
      src: app.conf.j2
      dest: /etc/app.conf
    notify: restart app

handlers:
  - name: restart app
    service:
      name: app
      state: restarted
```

---

## File: handler-playbook.yaml

Create this playbook:

```yaml
- name: Handler demonstration
  hosts: all
  become: true

  tasks:
    - name: Install httpd
      dnf:
        name: httpd
        state: present

    - name: Deploy custom httpd config
      copy:
        content: |
          # Managed by Ansible
          ServerName {{ ansible_hostname }}
        dest: /etc/httpd/conf.d/custom.conf
        mode: "0644"
      notify: restart httpd

  handlers:
    - name: restart httpd
      service:
        name: httpd
        state: restarted
```

---

## Running the Playbook

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini handler-playbook.yaml
```

First run:

- config file is created
- handler is notified
- httpd restarts

Second run:

- no config change
- handler is not triggered

---

## Multiple Tasks Notifying Same Handler

```yaml
notify: restart httpd
```

All tasks referencing the same handler name will trigger **one restart**.

---

## Forcing Handler Execution

Use `meta: flush_handlers` to run handlers immediately.

```yaml
- meta: flush_handlers
```

Use sparingly.

---

## Handlers with Conditions

Handlers can also have `when` conditions.

```yaml
handlers:
  - name: restart httpd
    service:
      name: httpd
      state: restarted
    when: ansible_os_family == "RedHat"
```

---

## Handlers vs Normal Tasks

| Normal Task      | Handler               |
| ---------------- | --------------------- |
| Runs immediately | Runs at end           |
| Runs every time  | Runs only if notified |
| Can repeat       | Runs once             |

---

## Common Mistakes

- Expecting handler to run without `notify`
- Misspelling handler name
- Restarting services in normal tasks
- Forgetting handlers run at end
- Using handlers for non-event actions

---

## Validation Checklist

You should be able to:

- Explain what a handler is
- Use notify correctly
- Understand handler execution timing
- Avoid unnecessary service restarts
- Use flush_handlers safely

---
