# postgresql

`postgresql` installs and initializes the PostgreSQL database server.

## Integrations

* Bundles:
  * [collectd](https://github.com/rullmann/bundlewrap-collectd)
    * collectd integration is turned off by default as it requires a user `collectd` to be present.

## Metadata

No metadata is required, but you can use the following options:

    'metadata': {
        'postgresql': {
            'collectd': False, # off by default. Add a role called collectd if you want to enable it (!)
            'roles': {
                'someuser': {
                    'password': 'somepassword',
                    'superuser': True, # optional, default is False
                },
            },
            'databases': {
                'somedatabase':{
                    'owner': 'someuser',
                },
            },
            'backup': True, # optional, backups via pg_back can be disabled
        },
    }

## Backups

This bundle is using [pg_back](https://github.com/orgrim/pg_back) to perform daily backups of all databases.
Currently backups can be disabled, but not configured.
