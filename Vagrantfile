# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "ubuntu/jammy64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  config.vm.synced_folder ".", "/var/www/replacement-twitter", mount_options: ["dmode=777,fmode=777"]

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
    vb.memory = "2048"
  end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
  apt-get update;
  curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -;
  apt install -y nodejs;
  apt-get install -y nginx vim uwsgi;
  apt-get install -y uwsgi-plugin-python3;
  apt-get install -y python3.10-venv;
  python3 -m venv /var/www/replacement-twitter/venv;
  apt-get install -y python3-pip;
  cd /var/www/replacement-twitter;
  mkdir account-static;
  touch db.sqlite3;
  source venv/bin/activate;
  pip install -r requirements.txt;
  python3 manage.py migrate;
  cp /var/www/replacement-twitter/Deployment/nginx.conf /etc/nginx/sites-enabled/default;
  cp /var/www/replacement-twitter/Deployment/uwsgi.ini /etc/uwsgi/apps-enabled/replacement-twitter.ini;
  mkdir /var/log/replacement-twitter;
  cd /var/www/replacement-twitter/frontend;
  npm install -g npm@latest;
  npm install;
  npm install -g @quasar/cli;
  quasar build;
  cd /var/www/replacement-twitter;
  service uwsgi restart;
  service nginx restart;
  SHELL
end
