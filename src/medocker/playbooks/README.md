# Medocker User Setup Playbook

This directory contains Ansible playbooks for setting up user workstations.

## Usage

1. Ensure Ansible is installed on your control machine:
   ```
   pip install ansible
   ```

2. Edit the inventory.yml file to include your target hosts
3. Run the playbook:
   ```
   ansible-playbook -i inventory.yml medocker-user-setup.yml
   ```

For more information, see the Medocker documentation.
