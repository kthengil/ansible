# Session 04 – YAML Basics for Ansible

---

## Why YAML in Ansible

Ansible uses YAML to describe **desired state** in a human-readable way.
YAML is:

- Indentation based
- Declarative
- Strict about structure
- Sensitive to whitespace

Every Ansible playbook, task file, variable file, and role uses YAML.

If YAML is wrong, Ansible **will not run**, regardless of how correct the logic is.

---

## YAML vs Programming Languages

YAML is **not a programming language**.
It has:

- No loops by itself
- No conditionals by itself
- No execution logic

YAML is only a **data representation format**.
Ansible adds logic on top of YAML.

---

## YAML File Structure

YAML files commonly contain:

- Dictionaries (key–value pairs)
- Lists
- Scalars (strings, numbers, booleans)

Indentation defines hierarchy.

---

## Indentation Rules (Critical)

- Use **spaces only**
- Do **not** use tabs
- Indentation must be consistent
- Common practice: 2 spaces per level

Correct:

```yaml
parent:
  child:
    key: value
```

Incorrect:

```yaml
parent:
  child:
    key: value
```

---

## Comments

Comments start with `#`

```yaml
# This is a comment
key: value # Inline comment
```

Comments are ignored by Ansible.

---

## Scalars (Simple Values)

Scalars are basic values.

```yaml
string_value: hello
number_value: 42
boolean_true: true
boolean_false: false
```

Quoted strings:

```yaml
quoted_string: "hello world"
single_quoted: "hello world"
```

---

## Dictionaries (Key–Value Pairs)

```yaml
user:
  name: sysansible
  shell: /bin/bash
  uid: 1001
```

Keys:

- Must be unique within the same level
- Are case-sensitive

---

## Lists

Lists start with `-`

```yaml
packages:
  - vim
  - git
  - curl
```

Inline list:

```yaml
packages: [vim, git, curl]
```

---

## List of Dictionaries

Very common in Ansible.

```yaml
users:
  - name: alice
    uid: 1001
  - name: bob
    uid: 1002
```

Each list item is its own dictionary.

---

## Mixing Lists and Dictionaries

```yaml
service:
  name: httpd
  state: started
  ports:
    - 80
    - 443
```

Hierarchy is defined purely by indentation.

---

## YAML Documents

YAML can contain multiple documents using `---`

```yaml
---
key1: value1
---
key2: value2
```

Ansible usually uses **one document per file**.

---

## Strings and Special Characters

Strings containing special characters should be quoted.

```yaml
path: "/var/www/html"
command: "echo hello > /tmp/file"
```

---

## Multiline Strings

### Literal block (`|`)

Preserves newlines.

```yaml
message: |
  Line one
  Line two
  Line three
```

### Folded block (`>`)

Newlines become spaces.

```yaml
message: >
  This is a long
  sentence split
  across lines
```

---

## Booleans – Common Pitfall

Valid booleans:

```yaml
true, false
yes, no
on, off
```

Best practice:

```yaml
enabled: true
```

---

## Numbers and Strings

```yaml
port: 80        # number
port: "80"      # string
```

Ansible treats them differently.

---

## Null Values

```yaml
key: null
key: ~
```

Used when a value is intentionally empty.

---

## YAML Anchors and Aliases (Advanced)

```yaml
defaults: &defaults
  owner: root
  mode: "0644"

file1:
  <<: *defaults
  path: /tmp/file1
```

Used rarely but useful in large configurations.

---

## YAML Validation (Manual)

Check indentation visually.
Check alignment of `-`.
Ensure consistent spacing.

Common YAML errors:

- Mixed tabs and spaces
- Incorrect list indentation
- Missing colon after key
- Misaligned blocks

---

## YAML in Ansible Context

Where YAML is used:

- Playbooks
- Tasks
- Variables
- Inventory (YAML format)
- Role files

YAML structure must match what the **Ansible module expects**.

---

## Common Beginner Mistakes

- Treating YAML like code
- Using tabs
- Misaligning lists
- Forgetting `-` for list items
- Incorrect nesting under `tasks`

---

## How to use the file

- From the session directory:
  `cat yaml-examples.yaml`
- Optional validation test:
  `python3 -c "import yaml; yaml.safe_load_all(open('yaml-examples.yaml'))"`

_(Only for learning — Ansible itself will validate YAML at runtime.)_

## Validation Checklist

You should be able to:

- Identify dictionaries and lists
- Write valid YAML by hand
- Understand indentation hierarchy
- Read and debug YAML errors
- Explain why YAML structure matters in Ansible

---
