# Session 02 – Inventory Fundamentals

---

## Objective

This session focuses on understanding how Ansible discovers and organizes managed nodes using inventories.

By the end of this session, you will:

- Understand what an inventory is and why it is required
- Use INI and YAML inventory formats
- Create host groups and nested groups
- Verify inventory parsing
- Run Ansible commands using a custom inventory

---

## What is an Inventory?

An inventory is a **list of managed nodes** that Ansible can target.

It answers three core questions:

- Which systems should Ansible manage?
- How are these systems grouped?
- How should Ansible connect to them?

Without an inventory, Ansible has no targets.

---

## Inventory Types

### Static Inventory

- Manually maintained
- INI or YAML format
- Most common in learning and small environments

### Dynamic Inventory

- Generated automatically
- Uses scripts or plugins
- Common with cloud providers

This session focuses on **static inventories**.

---

## Inventory Formats Supported

Ansible supports multiple formats:

- INI (most common, simplest)
- YAML (structured, extensible)
- JSON (less common)

---

## Lab Inventory Design

### Managed Nodes

- flame
- frost
- storm
- earth
- water

### Logical Grouping

- web → flame, frost
- db → storm
- app → earth, water
- prod → web + db
- nonprod → app

---

## INI Inventory Structure

Open the file:

```bash
inventory.ini
```

Key concepts:

- Groups are defined using `[groupname]`
- Hosts can belong to multiple groups
- Group nesting is done using `:children`

---

## YAML Inventory Structure

Open the file:

```bash
inventory.yaml
```

Key concepts:

- Uses dictionaries and lists
- Explicit hierarchy
- Easier to extend with variables later

---

## Using a Custom Inventory

Ansible does not automatically use files named `inventory.ini`.

You must specify it explicitly:

```bash
ansible -i inventory.ini all --list-hosts
```

---

## Verifying Inventory Parsing

### List all hosts

```bash
ansible -i inventory.ini all --list-hosts
```

### List hosts in a specific group

```bash
ansible -i inventory.ini web --list-hosts
```

---

## Running Commands Using Inventory

```bash
ansible -i inventory.ini all -m ping
```

```bash
ansible -i inventory.ini prod -m command -a "hostname"
```

---

## Inventory Graph View

To visually understand group relationships:

```bash
ansible-inventory -i inventory.ini --graph
```

Repeat with YAML inventory:

```bash
ansible-inventory -i inventory.yaml --graph
```

---

## Common Inventory Mistakes

- Forgetting `-i` option
- Incorrect group indentation in YAML
- Using tabs instead of spaces
- Duplicate hostnames
- Misusing `:children`

---

## Validation Checklist

You should be able to:

- Explain what an inventory is
- Create an INI inventory
- Create a YAML inventory
- Group hosts logically
- Run Ansible commands using a custom inventory
- Visualize inventory hierarchy

---

## What’s Next

In the next session, you will:

- Run real-world ad-hoc commands
- Use modules like dnf, service, copy
- Understand module idempotency

Proceed to:

```bash
/home/sysansible/lab/session03-ad-hoc-commands
```

````

---

## 📄 inventory.ini

```ini
# Inventory in INI format

[all]
flame
frost
storm
earth
water

[web]
flame
frost

[db]
storm

[app]
earth
water

[prod:children]
web
db

[nonprod:children]
app
````

---

## 📄 inventory.yaml

```yaml
all:
  hosts:
    flame:
    frost:
    storm:
    earth:
    water:

  children:
    web:
      hosts:
        flame:
        frost:

    db:
      hosts:
        storm:

    app:
      hosts:
        earth:
        water:

    prod:
      children:
        web:
        db:

    nonprod:
      children:
        app:
```

---

## ✅ Quick Verification Commands

Run from this directory:

```bash
ansible -i inventory.ini all -m ping
ansible -i inventory.yaml prod -m command -a "hostname"
ansible-inventory -i inventory.ini --graph
ansible-inventory -i inventory.yaml --graph
```
