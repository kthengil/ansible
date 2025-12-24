# Session 05 – First Ansible Playbook

## What a Playbook Is

A playbook is a **YAML file** that describes:

- which hosts to target
- what tasks to execute
- in what order
- using which modules

Playbooks are **declarative**:
You describe the desired state, not the steps to reach it.

---

## Anatomy of a Playbook

A playbook is a **list of plays**.

Each play contains:

- hosts
- become (optional)
- tasks

Basic structure:

```yaml
- name: Play description
  hosts: target_hosts
  become: true
  tasks:
    - name: Task description
      module_name:
        option: value
```

````

Indentation defines hierarchy.
Incorrect indentation = invalid playbook.

---

## Inventory Used in This Session

This session uses a dedicated inventory file.

Managed nodes:

- flame
- frost
- storm
- earth
- water

Groups are defined for testing.

---

## File: inventory.ini

Create or open `inventory.ini`:

```ini
[all]
flame
frost
storm
earth
water

[web]
flame
frost
```

---

## First Playbook Goals

This playbook will:

- target all managed nodes
- run as root (via become)
- install a package
- ensure a service is running
- create a file to prove execution

---

## File: first-playbook.yaml

```yaml
- name: First Ansible Playbook
  hosts: all
  become: true

  tasks:
    - name: Install httpd package
      dnf:
        name: httpd
        state: present

    - name: Ensure httpd service is started
      service:
        name: httpd
        state: started
        enabled: true

    - name: Create a test file
      copy:
        content: "This system is managed by Ansible\n"
        dest: /tmp/ansible-session5.txt
        owner: root
        group: root
        mode: "0644"
```

---

## Running the Playbook

From the session directory:

```bash
ansible-playbook -i inventory.ini first-playbook.yaml
```

Observe:

- task order
- changed status
- ok status
- failed tasks (if any)

---

## Understanding Task Output

- **ok** → task already satisfied desired state
- **changed** → task made a change
- **failed** → task could not complete
- **skipped** → task was skipped due to conditions (later sessions)

---

## Dry Run (Check Mode)

Simulate execution without making changes:

```bash
ansible-playbook -i inventory.ini first-playbook.yaml --check
```

This helps:

- validate logic
- preview changes
- avoid accidental modifications

---

## Diff Mode

Show file differences when files change:

```bash
ansible-playbook -i inventory.ini first-playbook.yaml --diff
```

Useful for:

- configuration files
- templates
- audits

---

## Limiting Playbook Execution

Run on a single host:

```bash
ansible-playbook -i inventory.ini first-playbook.yaml --limit flame
```

Run on a group:

```bash
ansible-playbook -i inventory.ini first-playbook.yaml --limit web
```

---

## Re-running the Playbook (Idempotency)

Run the playbook again:

```bash
ansible-playbook -i inventory.ini first-playbook.yaml
```

Expected behavior:

- Most tasks report **ok**
- No unnecessary changes occur

This confirms idempotency.

---

## Common Beginner Mistakes

- Forgetting `-i inventory.ini`
- Using tabs instead of spaces
- Incorrect indentation under `tasks`
- Using `shell` instead of modules
- Forgetting `become: true`

---

## Validation Checklist

You should be able to:

- Explain play vs task
- Write a valid playbook
- Run a playbook successfully
- Interpret playbook output
- Use check and diff mode
- Limit playbook execution

---
````
