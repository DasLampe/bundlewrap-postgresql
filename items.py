pkg_yum = {
    "postgresql": {},
    "postgresql-server": {
    },
}

svc_systemd = {
    'postgresql': {
        'enabled': True,
        'needs': [
            "pkg_yum:postgresql-server",
            "action:postgresql_initdb",
        ],
    },
}

files = {
    '/var/lib/pgsql/data/pg_hba.conf': {
        'source': "pg_hba.conf",
        'owner': "postgres",
        'group': "postgres",
        'mode': "0600",
        'needs': [
            "pkg_yum:postgresql-server",
        ],
        'triggers': [
            "svc_systemd:postgresql:restart",
        ],
    },
}

actions = {
    'postgresql_initdb': {
        'command': "postgresql-setup --initdb --unit postgresql",
        'unless': "ls /var/lib/pgsql/initdb_postgresql.log",
        'needs': [
            "pkg_yum:postgresql-server",
            "file:/var/lib/pgsql/data/pg_hba.conf"
        ],
    },
}

postgres_roles = {}

for role in node.metadata.get('postgresql', {}).get('roles', []):
    postgres_roles[role['name']] = {
        'superuser': role.get('superuser', False),
        'password': role['password'],
    }

postgres_dbs = {}

for db in node.metadata.get('postgresql', {}).get('databases', []):
    postgres_dbs[db['name']] = {
        'owner': db.get('owner', 'postgres'),
    }