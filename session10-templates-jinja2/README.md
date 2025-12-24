# Session 10 – Templates and Jinja2

---

## Why Templates Are Needed

Templates allow Ansible to generate **dynamic configuration files**.

Without templates:

- files are static
- environment-specific changes require multiple files
- logic leaks into playbooks

With templates:

- one template works for many hosts
- values come from variables and facts
- configuration stays consistent and scalable

Templates use **Jinja2** syntax.

---

## What Is a Template

A template is a text file (usually `.j2`) that contains:

- plain text
- variables
- expressions
- conditionals
- loops

At runtime:

- Ansible renders the template
- replaces variables with values
- copies the final file to the managed node

---

## Template Module

Ansible uses the `template` module.

Basic syntax:

```yaml
- name: Render configuration
  template:
    src: template_file.j2
    dest: /path/to/file
```

---

## Jinja2 Variable Syntax

Variables are referenced using:

```jinja
{{ variable_name }}
```

Example:

```jinja
Application name: {{ app_name }}
```

---

## File: templates/app.conf.j2

Create this template file:

```jinja
# Application Configuration
# Managed by Ansible

app_name={{ app_name }}
app_env={{ environment }}
app_port={{ app_port }}

hostname={{ ansible_hostname }}
os_family={{ ansible_os_family }}
```

---

## Using Variables in Templates

Templates can use:

- playbook variables
- vars files
- inventory variables
- facts

No special declaration is required.

---

## Conditional Logic in Templates

Use `{% if %}` blocks.

```jinja
{% if environment == "production" %}
log_level=ERROR
{% else %}
log_level=DEBUG
{% endif %}
```

Only one branch is rendered.

---

## Loops in Templates

Use `{% for %}` loops.

```jinja
{% for pkg in packages %}
package={{ pkg }}
{% endfor %}
```

Each iteration renders a new line.

---

## Whitespace Control

Jinja2 respects whitespace.

Be careful with indentation and newlines.

To trim whitespace:

```jinja
{%- for item in items -%}
{{ item }}
{%- endfor -%}
```

Use trimming sparingly.

---

## File: template-playbook.yaml

Create this playbook:

```yaml
- name: Template rendering demonstration
  hosts: all
  become: true

  vars:
    app_name: demo_app
    environment: dev
    app_port: 8080

    packages:
      - vim
      - git
      - curl

  tasks:
    - name: Create application directory
      file:
        path: /opt/demo_app
        state: directory
        mode: "0755"

    - name: Render application configuration
      template:
        src: templates/app.conf.j2
        dest: /opt/demo_app/app.conf
        owner: root
        group: root
        mode: "0644"
```

---

## Running the Playbook

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini template-playbook.yaml
```

---

## Inspect Rendered Output

On any managed node:

```bash
cat /opt/demo_app/app.conf
```

You should see:

- variables replaced with values
- hostname and OS facts populated
- clean, readable configuration

---

## Overriding Template Variables

Override at runtime:

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini \
template-playbook.yaml \
-e "environment=production app_port=9090"
```

Re-check the rendered file.

---

## Template vs Copy

| copy           | template          |
| -------------- | ----------------- |
| Static files   | Dynamic files     |
| No logic       | Supports logic    |
| Simple content | Configurations    |
| No variables   | Variables + facts |

Use `copy` when no logic is required.

---

## Common Mistakes

- Using `{{ }}` inside `{% %}`
- Forgetting that templates are rendered on control node
- Hardcoding values inside templates
- Incorrect indentation causing malformed config
- Mixing YAML and Jinja syntax

---

## Validation Checklist

You should be able to:

- Explain what a template is
- Use variables and facts in templates
- Use conditionals and loops in templates
- Render files using the template module
- Override template values safely
- Inspect and validate rendered output

---
