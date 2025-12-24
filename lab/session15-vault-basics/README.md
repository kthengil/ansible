# Session 15 – Ansible Vault Basics

---

## Why Vault Is Required

Automation often needs secrets:

- passwords
- API keys
- tokens
- private configuration values

Storing secrets in plain text is unsafe.
Ansible Vault allows you to **encrypt sensitive data** while keeping playbooks usable.

---

## What Is Ansible Vault

Ansible Vault:

- encrypts files or variables
- integrates directly with Ansible
- allows secure sharing of automation code
- supports partial or full encryption

Vault encryption uses a password.

---

## What Should Be Encrypted

Good candidates:

- passwords
- secrets
- API tokens
- private keys (with care)

Do not encrypt:

- entire playbooks unnecessarily
- non-sensitive configuration

Encrypt only what must be protected.

---

## Creating an Encrypted File

Create a new encrypted variables file:

```bash
ansible-vault create secret-vars.yaml
```

You will be prompted for a password.

---

## File: secret-vars.yaml (Encrypted)

After encryption, the file looks like:

```yaml
$ANSIBLE_VAULT;1.1;AES256
6638663438306636663434666139656238306135396233303434303163643837333339
3263303434303430323533366462363861346433363964383433310a65396637313230
```

The content is unreadable without the password.

---

## Editing an Encrypted File

```bash
ansible-vault edit secret-vars.yaml
```

Decrypts temporarily, opens editor, re-encrypts on save.

---

## Viewing an Encrypted File

```bash
ansible-vault view secret-vars.yaml
```

Read-only access.

---

## Encrypting an Existing File

```bash
ansible-vault encrypt vars.yaml
```

Decrypt later:

```bash
ansible-vault decrypt vars.yaml
```

---

## Using Vault Variables in a Playbook

Create this playbook:

`vault-playbook.yaml`

```yaml
- name: Vault variable demonstration
  hosts: all
  become: true
  vars_files:
    - secret-vars.yaml

  tasks:
    - name: Show masked secret usage
      copy:
        content: |
          db_user={{ db_user }}
          db_password={{ db_password }}
        dest: /tmp/secret_info.txt
        mode: "0600"
```

Variables `db_user` and `db_password` are stored in the vault file.

---

## Running a Vault-Protected Playbook

Prompt for password:

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini \
vault-playbook.yaml \
--ask-vault-pass
```

---

## Using a Vault Password File

Create a password file:

```bash
echo "vaultpassword" > ~/.vault_pass
chmod 600 ~/.vault_pass
```

Run playbook:

```bash
ansible-playbook -i ../session05-first-playbook/inventory.ini \
vault-playbook.yaml \
--vault-password-file ~/.vault_pass
```

---

## Encrypting Only a Variable (Inline Vault)

```bash
ansible-vault encrypt_string 'mypassword' --name 'db_password'
```

Output example:

```yaml
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  62303138333031376663353534636637383262356566356533353562346238626232
```

Can be pasted directly into vars files.

---

## Multiple Vault Passwords (Intro)

Ansible supports:

- multiple vault IDs
- multiple passwords

Used in advanced setups.

---

## Best Practices

- Encrypt only secrets
- Never commit vault password files
- Use environment-specific vaults
- Rotate secrets periodically
- Use version control with vault safely

---

## Common Mistakes

- Encrypting entire playbooks
- Losing vault password
- Hardcoding vault password in scripts
- Using weak passwords
- Mixing encrypted and plain secrets carelessly

---

## Validation Checklist

You should be able to:

- Create encrypted files
- Edit and view vault files
- Use vault variables in playbooks
- Run vault-protected playbooks
- Understand vault best practices

---
