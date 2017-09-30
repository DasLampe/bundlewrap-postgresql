pkg_dnf = {
    'postgresql': {},
    'postgresql-server': {
    },
}

svc_systemd = {
    'postgresql': {
        'needs': ['pkg_dnf:postgresql-server', 'action:postgresql_initdb'],
    },
}

files = {
    '/var/lib/pgsql/data/pg_hba.conf': {
        'source': 'pg_hba.conf',
        'owner': 'postgres',
        'group': 'postgres',
        'mode': '0600',
        'needs': ['pkg_dnf:postgresql-server'],
        'triggers': ['svc_systemd:postgresql:restart'],
    },
}

actions = {
    'postgresql_initdb': {
        'command': 'postgresql-setup --initdb --unit postgresql',
        'unless': 'ls /var/lib/pgsql/initdb_postgresql.log',
        'needs': ['pkg_dnf:postgresql-server'],
    },
}

postgres_roles = {}

postgres_dbs = {}

for name, config in node.metadata.get('postgresql', {}).get('roles', {}).items():
    postgres_roles[name] = {
        'superuser': config.get('superuser', False),
        'password': config['password'],
        'needs': ['pkg_dnf:postgresql-server', 'action:postgresql_initdb'],
    }

for name, config in node.metadata.get('postgresql', {}).get('databases', {}).items():
    postgres_dbs[name] = {
        'owner': config.get('owner', 'postgres'),
        'needs': ['pkg_dnf:postgresql-server', 'action:postgresql_initdb'],
    }

if node.has_bundle('monit'):
    files['/etc/monit.d/postgresql'] = {
        'source': 'monit',
        'mode': '0640',
        'triggers': ['svc_systemd:monit:restart'],
    }

if node.has_bundle('collectd') and node.metadata.get('postgresql', {}).get('collectd', False):

    pkg_dnf['collectd-postgresql'] = {}

    files['/etc/collectd.d/postgresql.conf'] = {
        'source': 'collectd.conf',
        'mode': '0640',
        'content_type': 'mako',
        'needs': ['pkg_dnf:collectd-postgresql'],
        'triggers': ['svc_systemd:collectd:restart'],
    }
