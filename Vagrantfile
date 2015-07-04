unless Vagrant.has_plugin?("vagrant-shortcuts") and VagrantShortcuts::VERSION >= "0.2.0"
  raise <<-help
vagrant-shortcuts is not installed, or is outdated! Run:

    $ vagrant plugin install vagrant-shortcuts
  help
end

Vagrant.configure("2") do |config|

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 1
    v.gui = true
  end

  config.vm.box = "ubuntu/trusty64"

  config.vm.network :forwarded_port,
    id: "http",
    guest: 8000,
    host: 8003
  config.vm.network :forwarded_port,
    id: "ssh",
    guest: 22,
    host: 8001
  config.vm.network :forwarded_port,
    id: "elasticsearch",
    guest: 9200,
    host: 8002

  config.vm.provision :shell,
    :path => "setup/install.sh"

  config.shortcuts.add(:assets) do |machine|
    machine.action(:ssh_run, ssh_run_command: <<-cmd)
      source ~/.bashrc.vagrant
      gulp watch
    cmd
  end

  config.shortcuts.add(:runserver) do |machine|
    machine.action(:ssh_run, ssh_run_command: <<-cmd)
      source ~/.bashrc.vagrant
      ./manage.py runserver
    cmd
  end

  config.shortcuts.add(:build) do |machine|
    machine.action(:ssh_run, ssh_run_command: <<-cmd)
      source ~/.bashrc.vagrant
      ./setup.py sdist
    cmd
  end

  if File.exist? "Vagrantfile.local"
    instance_eval File.read("Vagrantfile.local"), "Vagrantfile.local"
  end
end


# vi: set ft=ruby sw=2 ts=2 :
