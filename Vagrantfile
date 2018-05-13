Vagrant.configure("2") do |config|

  config.vm.box = "terrywang/archlinux"
  config.vm.synced_folder "pycon", "/srv/pycon", type: "rsync"
  config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.provision "shell", path: "setup.sh"
end
