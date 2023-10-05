# Puppet for setup
exec { 'apt-update':
  command     => '/usr/bin/apt-get -y update',
  refreshonly => true,
}

exec { 'hbnb':
    command     => sed -i '61i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default,
}

package { 'nginx':
  ensure   => 'present',
}

file { '/data':
  ensure  => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}
file { '/data/web_static/releases/test':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "fake test file to check nginx \n"
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/',
}
file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
}

service { 'nginx':
  ensure => 'running',
}