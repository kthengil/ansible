# Session 17 – Capstone Project (End-to-End Automation)

---

## Capstone Goal

Design and implement a **production-style Ansible project** that combines everything learned so far:

- inventories
- variables and facts
- conditionals and loops
- templates
- handlers
- error handling
- roles
- includes/imports
- vault (optional)
- troubleshooting mindset

This session focuses on **design first, then implementation**.

---

## Problem Statement

Automate the deployment of a **simple web application stack** with the following requirements:

- Target group: `web`
- Install and configure `httpd`
- Deploy a dynamic configuration using templates
- Serve a simple index page with host-specific content
- Restart service only when configuration changes
- Handle failures gracefully
- Keep code modular and reusable

---

## Project Directory Structure

```text
session17-capstone-project/
├── README.md
├── inventory.ini
├── site.yaml
├── group_vars/
│   └── web.yaml
└── roles/
    └── webstack/
        ├── defaults/
        │   └── main.yaml
        ├── vars/
        │   └── main.yaml
        ├── tasks/
        │   ├── install.yaml
        │   ├── config.yaml
        │   ├── content.yaml
        │   └── main.yaml
        ├── handlers/
        │   └── main.yaml
        └── templates/
            ├── httpd.conf.j2
            └── index.html.j2
```

---

## Inventory Design

File: `inventory.ini`

```ini
[web]
flame
frost
```

---

## Group Variables

File: `group_vars/web.yaml`

```yaml
web_package: httpd
web_service: httpd
web_root: /var/www/html

app_name: demo_web_app
environment: production
```

---

## Role Defaults

File: `roles/webstack/defaults/main.yaml`

```yaml
http_port: 80
```

Defaults are safe, overridable values.

---

## Role Vars

File: `roles/webstack/vars/main.yaml`

```yaml
httpd_conf_dir: /etc/httpd/conf.d
```

Vars have higher precedence; use sparingly.

---

## Role Task Structure

### File: `roles/webstack/tasks/main.yaml`

```yaml
- import_tasks: install.yaml
- import_tasks: config.yaml
- import_tasks: content.yaml
```

---

### File: `roles/webstack/tasks/install.yaml`

```yaml
- name: Install web server package
  dnf:
    name: "{{ web_package }}"
    state: present
```

---

### File: `roles/webstack/tasks/config.yaml`

```yaml
- name: Deploy httpd configuration
  template:
    src: httpd.conf.j2
    dest: "{{ httpd_conf_dir }}/ansible.conf"
    mode: "0644"
  notify: restart web service
```

---

### File: `roles/webstack/tasks/content.yaml`

```yaml
- name: Deploy application index page
  template:
    src: index.html.j2
    dest: "{{ web_root }}/index.html"
    mode: "0644"
```

---

## Templates

### File: `roles/webstack/templates/httpd.conf.j2`

```jinja
# Managed by Ansible

Listen {{ http_port }}

<VirtualHost *:{{ http_port }}>
    DocumentRoot "{{ web_root }}"
    ServerName {{ ansible_hostname }}
</VirtualHost>
```

---

### File: `roles/webstack/templates/index.html.j2`

```jinja
<html>
<head>
  <title>{{ app_name }}</title>
</head>
<body>
  <h1>{{ app_name }}</h1>
  <p>Environment: {{ environment }}</p>
  <p>Served from host: {{ ansible_hostname }}</p>
</body>
</html>
```

---

## Handlers

File: `roles/webstack/handlers/main.yaml`

```yaml
- name: restart web service
  service:
    name: "{{ web_service }}"
    state: restarted
```

---

## Site Playbook

File: `site.yaml`

```yaml
- name: Deploy web stack
  hosts: web
  become: true

  roles:
    - webstack
```

---

## Running the Capstone Project

From the capstone directory:

```bash
ansible-playbook -i inventory.ini site.yaml
```

Re-run to confirm:

- idempotency
- handler only runs on change

---

## Validation Steps

On managed nodes:

```bash
systemctl status httpd
```

From control node:

```bash
curl http://flame
curl http://frost
```

Verify:

- dynamic hostname rendering
- correct environment value
- service stability

---

## Failure Handling Considerations

Enhancements you can add:

- wrap install/config tasks in `block/rescue`
- add health checks
- add rollback markers
- add `failed_when` logic

---

## Design Review Checklist

You should be able to explain:

- why roles were used
- why defaults vs vars were chosen
- why handlers are triggered only on change
- how templates enable reuse
- how includes structure tasks
- how inventory + group_vars drive behavior

---

## What You Have Achieved

You now understand:

- full Ansible workflow
- enterprise-style project layout
- reusable automation design
- safe and idempotent execution
- troubleshooting and recovery patterns

This capstone mirrors **real production automation**.

---
