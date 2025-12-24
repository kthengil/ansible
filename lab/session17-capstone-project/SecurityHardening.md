# 🔐 Security Hardening (Capstone Extension)

## Goals

- Reduce attack surface
- Enforce least privilege
- Apply safe defaults
- Avoid unnecessary exposure
- Keep automation idempotent

---

## Hardening Strategy Applied

- Restrict file permissions
- Disable directory listing
- Add basic HTTP security headers
- Ensure firewall rules exist (if firewalld is present)
- Ensure services run only if required

---

## Update: `roles/webstack/defaults/main.yaml`

Add security-related defaults:

```yaml
http_port: 80
disable_directory_listing: true
enable_firewalld: true
```

---

## Update: `roles/webstack/tasks/config.yaml`

Replace existing content with **security-aware configuration**:

```yaml
- name: Deploy httpd configuration with hardening
  template:
    src: httpd.conf.j2
    dest: "{{ httpd_conf_dir }}/ansible.conf"
    mode: "0644"
    owner: root
    group: root
  notify: restart web service
```

---

## Update: `roles/webstack/templates/httpd.conf.j2`

Replace template with hardened version:

```jinja
# Managed by Ansible

ServerTokens Prod
ServerSignature Off

Listen {{ http_port }}

<VirtualHost *:{{ http_port }}>
    DocumentRoot "{{ web_root }}"
    ServerName {{ ansible_hostname }}

{% if disable_directory_listing %}
    <Directory "{{ web_root }}">
        Options -Indexes
        AllowOverride None
        Require all granted
    </Directory>
{% endif %}

    Header always set X-Content-Type-Options "nosniff"
    Header always set X-Frame-Options "DENY"
    Header always set X-XSS-Protection "1; mode=block"
</VirtualHost>
```

This introduces:

- conditional hardening
- security headers
- directory listing protection

---

## Optional: Firewalld Hardening

### File: `roles/webstack/tasks/firewall.yaml`

```yaml
- name: Ensure firewalld is installed
  dnf:
    name: firewalld
    state: present

- name: Ensure firewalld is running
  service:
    name: firewalld
    state: started
    enabled: true

- name: Allow HTTP port
  firewalld:
    port: "{{ http_port }}/tcp"
    permanent: true
    state: enabled
    immediate: true
```

---

### Update: `roles/webstack/tasks/main.yaml`

```yaml
- import_tasks: install.yaml
- import_tasks: config.yaml
- import_tasks: content.yaml
- import_tasks: firewall.yaml
  when: enable_firewalld
```

---

# 🖥️ OS-Based Conditionals

## Why OS Conditionals Matter

- Different OS families behave differently
- Modules, paths, services may vary
- Production automation must adapt safely

---

## Example: OS-Aware Package Installation

### Update: `roles/webstack/tasks/install.yaml`

```yaml
- name: Install web server on RedHat family
  dnf:
    name: "{{ web_package }}"
    state: present
  when: ansible_os_family == "RedHat"
```

---

## Example: OS-Specific Configuration Path

Add to `roles/webstack/vars/main.yaml`:

```yaml
httpd_conf_dir: >-
  {{ '/etc/httpd/conf.d'
     if ansible_os_family == 'RedHat'
     else '/etc/apache2/conf-enabled' }}
```

---

## Example: OS-Based Service Handling

```yaml
- name: Ensure web service is running
  service:
    name: "{{ web_service }}"
    state: started
    enabled: true
  when: ansible_service_mgr in ['systemd']
```

---

## Validation

```bash
ansible -i inventory.ini web -m setup -a "filter=ansible_os_family"
```

---

# 📊 Monitoring Hooks

## Monitoring Philosophy

This capstone adds **hooks**, not a full monitoring stack.

Goals:

- Detect service health
- Leave breadcrumbs for monitoring tools
- Enable easy integration with Nagios / Prometheus / Zabbix later

---

## Health Check File (Simple Hook)

### File: `roles/webstack/tasks/monitoring.yaml`

```yaml
- name: Create monitoring directory
  file:
    path: /opt/monitoring
    state: directory
    mode: "0755"

- name: Create health check file
  copy:
    content: |
      service=httpd
      status=running
      host={{ ansible_hostname }}
      timestamp={{ ansible_date_time.iso8601 }}
    dest: /opt/monitoring/web_health.txt
    mode: "0644"
```

---

### Update: `roles/webstack/tasks/main.yaml`

```yaml
- import_tasks: install.yaml
- import_tasks: config.yaml
- import_tasks: content.yaml
- import_tasks: firewall.yaml
  when: enable_firewalld
- import_tasks: monitoring.yaml
```

---

## HTTP Health Endpoint (Optional)

Add to `index.html.j2`:

```jinja
<!-- health: OK -->
```

Monitoring systems can grep this marker.

---

## Service Validation Hook

Add a post-task check:

```yaml
- name: Verify web service is reachable locally
  command: curl -s http://localhost
  register: web_check
  failed_when: web_check.rc != 0
  changed_when: false
```

This makes failures **explicit and visible**.

---

# ✅ Final Capstone Enhancements Summary

You now have:

✔ Security-hardened configuration
✔ Conditional OS-aware logic
✔ Monitoring integration hooks
✔ Production-style defensive automation
✔ Clean separation of concerns

This is **enterprise-grade Ansible design**.
