# postgresql

`postgresql` installs and initializes the PostgreSQL database server.

## Compatibility

This bundle has been tested on the following systems:

| OS          | `[x]` |
| ----------- | ----- |
| Fedora 24   | `[x]` |
| Fedberry 24 | `[X]` |

## Metadata

No metadata is required, but you can use the following options:

    'metadata': {
        'postgresql': {
            'roles': [
                {
                    'name': 'someuser',
                    'password': 'secret',
                    'superuser': True, # optional, default is False
                },
            ],
            'databases': [
                {
                    'name': 'somedatabase',
                    'owner': 'someuser',
                },
            ],
        },
    }
