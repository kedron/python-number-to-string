# Convenience packages installed on all servers.  TODO: move these to a common module
package { [ 'vim-enhanced', 'openssh-clients', 'mlocate', 'bind-utils' ]:
    ensure  => present,
}

# Project Specific Packages and Configuration

# python-tools - installs pygettext.py and msgfmt.py used to build message catalogs from python source.
# gettext - GNU i18n/l10n utilities - useful for building message catalogs from non-python source.
#package { [ 'python-tools', 'gettext', 'centos-release-SCL']:
#    ensure      => present,
#}

# Epel repo is needed for pip
package { 'epel':
    ensure      => present,
#    source      => 'http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm',
    source      => 'http://dl.fedoraproject.org/pub/epel/beta/7/x86_64/epel-release-7-0.2.noarch.rpm',
    provider    => rpm,
}

# pip is needed to install python modules
package { 'python-pip':
    ensure      => present,
    require     => Package['epel'],
}

# babel - i18n module for python
# flask - REST framework for python
package { [ 'babel', 'flask' ]:
    ensure      => present,
    provider    => pip,
    require     => Package['python-pip'],
}
