pkg_dnf = {
    "postgresql": {},
    "postgresql-server": {
    },
}

svc_systemd = {
    'postgresql': {
        'enabled': True,
        'needs': [
            "pkg_dnf:postgresql-server",
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
            "pkg_dnf:postgresql-server",
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
            "pkg_dnf:postgresql-server",
        ],
    },
}

postgres_roles = {}

for role in node.metadata.get('postgresql', {}).get('roles', []):
    postgres_roles[role['name']] = {
        'superuser': role.get('superuser', False),
        'password': role['password'],
        'needs': [
            "pkg_dnf:postgresql-server",
            "action:postgresql_initdb",
        ],
    }

postgres_dbs = {}

for db in node.metadata.get('postgresql', {}).get('databases', []):
    postgres_dbs[db['name']] = {
        'owner': db.get('owner', 'postgres'),
        'needs': [
            "pkg_dnf:postgresql-server",
            "action:postgresql_initdb",
        ],
    }

if node.has_bundle("monit"):
    files['/etc/monit.d/postgresql'] = {
        'source': "monit",
        'mode': "0640",
        'owner': "root",
        'group': "root",
        'triggers': [
            "svc_systemd:monit:restart",
        ],
    }
