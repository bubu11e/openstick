# OpenStick
A simple tool to manage a pool of VMs using Qemu/KVM. Because sometimes you don't need a full stack.

# Installation
    pip3 install openstick

# Configuration
OpenStick use by default a configuration file (~/.openstick) with INI structure. A DEFAULT section can be used to specify parameters to apply to all the VMs.

Sample:
-------------------------
    [DEFAULT]
    ports = 22,80,443,16852

    [carl]
    memory = 2G
-------------------------

# ToDo
- Intelligent port generator (Take into account )
- Check if the default name is not already in use
- Add tools to list running VMs
- Add tools to get corresponding forwarded port for a VM
- Add tools to list ports used by a VM
- Add tools to connect to a VM with ssh using it's name
- Add tools to connect to mount the root of a VM in a sub-folder using the name of the VM.
