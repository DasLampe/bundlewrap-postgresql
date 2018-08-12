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

directories = {}

git_deploy = {}

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

if node.metadata.get('postgresql', {}).get('backup', True):
    directories['/opt/pg_back'] = {}
    directories['/var/lib/pgsql/backups'] = {
        'owner': 'postgres',
        'mode': '0700',
        'needs': ['pkg_dnf:postgresql-server', ],
    }
    git_deploy['/opt/pg_back'] = {
        'needs': ['pkg_dnf:postgresql-server', 'directory:/opt/pg_back'],
        'repo': 'https://github.com/orgrim/pg_back.git',
        'rev': 'master',
    }
    files['/opt/pg_back/pg_back.conf'] = {
        'needs': ['pkg_dnf:postgresql-server', 'git_deploy:/opt/pg_back'],
    }
    files['/etc/cron.d/pg_back'] = {
        'source': 'pg_back.cron',
        'needs': ['pkg_dnf:postgresql-server', 'file:/opt/pg_back/pg_back.conf'],
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
