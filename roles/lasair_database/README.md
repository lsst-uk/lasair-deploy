Role Name
=========

Role for initial setup of the Lasair database.

Role Variables
--------------

`mysql_root_password`: MysQL/MariaDB root password
`mysql_db_name`: Database name
`mysql_db_user`: Username for full read/write access
`mysql_db_password`: Password for above
`msql_db_user_readonly`: Username for read only access
`mysql_db_password_readonly`: Password for above

The `settings` dict in defaults contains reasonable values for testing and can be overridden in production using values from Vault.

Example Playbook
----------------

    # Apply to either standalone DB host or the first Galera backend
    - hosts: db,backend_db[0]
      vars_files:
        - settings.yaml
      vars:
        settings: "{{ lookup('hashi_vault', 'secret='+vault.path+'/settings url='+vault.url)}}"
      roles:
        - lasair_database

License
-------

Apache-2.0

