# Session 14 – Includes and Imports

## Why Includes and Imports Are Needed

As automation grows:

- single task files become large
- logic becomes hard to read
- reuse becomes difficult

Includes and imports allow you to:

- split large files into smaller logical units
- reuse task files
- control execution behavior
- improve readability and maintenance

---

## Include vs Import (High-Level)

| Feature             | include | import     |
| ------------------- | ------- | ---------- |
| Evaluation time     | Runtime | Parse time |
| Conditional support | Yes     | Limited    |
| Loop support        | Yes     | No         |
| Dynamic behavior    | Yes     | No         |
| Static behavior     | No      | Yes        |

Modern best practice:

- use **import** for static structure
- use **include** for dynamic behavior

---

## Task File Organization Example

```text
tasks/
├── install.yaml
├── config.yaml
└── service.yaml
```

Each file contains a logical set of tasks.

---

## `import_tasks`

Used for static inclusion.

```yaml
- import_tasks: tasks/install.yaml
```

- Loaded at playbook parse time
- Cannot be conditional per task
- Best for fixed structure

---

## `include_tasks`

Used for dynamic inclusion.

```yaml
- include_tasks: tasks/config.yaml
```

- Loaded at runtime
- Can be conditional
- Can be looped

---

## File: tasks/install.yaml

```yaml
- name: Install httpd
  dnf:
    name: httpd
    state: present
```

---

## File: tasks/config.yaml

```yaml
- name: Deploy configuration file
  copy:
    content: |
      # Managed by Ansible
      ServerName {{ ansible_hostname }}
    dest: /etc/httpd/conf.d/include.conf
    mode: "0644"
```

---

## File: tasks/service.yaml

```yaml
- name: Ensure httpd is running
  service:
    name: httpd
    state: started
    enabled: true
```

---

## File: main.yaml

```yaml
- name: Modular playbook using includes and imports
  hosts: all
  become: true

  tasks:
    - name: Install phase
      import_tasks: tasks/install.yaml

    - name: Configuration phase
      include_tasks: tasks/config.yaml

    - name: Service phase
      import_tasks: tasks/service.yaml
```

---

## Conditional Includes

```yaml
- include_tasks: tasks/config.yaml
  when: ansible_os_family == "RedHat"
```

This is **not possible** with `import_tasks`.

---

## Looping Includes

```yaml
- include_tasks: tasks/config.yaml
  loop:
    - conf1
    - conf2
```

Each iteration re-includes the file.

---

## Import vs Include – Practical Guidance

Use `import_tasks` when:

- structure is fixed
- tasks should always exist
- roles are stable

Use `include_tasks` when:

- behavior changes at runtime
- conditionals are needed
- looping is required

---

## Include vs Roles

| Include              | Role                |
| -------------------- | ------------------- |
| Lightweight          | Structured          |
| Task-level reuse     | Feature-level reuse |
| No defaults/handlers | Full feature set    |
| Good inside roles    | Best for projects   |

Includes are often used **inside roles**.

---

## Common Mistakes

- Using include when import is better
- Expecting import to be conditional
- Over-splitting tasks into tiny files
- Mixing include and import without purpose
- Forgetting variable scope

---

## Validation Checklist

You should be able to:

- Explain include vs import differences
- Use import_tasks correctly
- Use include_tasks with conditions
- Split large task files logically
- Choose correct technique for reuse

---
