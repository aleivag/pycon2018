Vagrant.configure("2") do |config|

  config.vm.box = "aleivag/arch64"
  config.vm.box_version = "2018.10.07"
  config.vm.synced_folder "pycon", "/srv/pycon", type: "rsync"
  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.provision "shell", path: "setup.sh"
end
