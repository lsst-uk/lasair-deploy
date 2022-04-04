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

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

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

