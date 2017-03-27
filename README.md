# openstick
A simple tool to manage a pool of VMs using Qemu/KVM.

usage: openstick [-h] [-b BOOT] [-c CORES] [-d DISK] [-e DOMAINS]
                 [--file CONFIGURATION_FILE_PATH] [-f FORMAT] [-j HOSTNAME]
                 [-i IMAGE] [-m MEMORY] [-n NAME] [-p PORTS]
                 [-r ROOT_IMAGE_PATH] [-s SIZE] [-u SOCKETS] [-t THREADS]

Because sometimes you don't need a full stack

optional arguments:
  -h, --help            show this help message and exit
  -b BOOT, --boot BOOT  Boot option. Can be hdd, cdrom or network.
  -c CORES, --cores CORES
                        Number of cores for the virtual machine.
  -d DISK, --disk DISK  Path to a disk image
  -e DOMAINS, --domains DOMAINS
                        DNS to look for.
  --file CONFIGURATION_FILE_PATH
                        Path to the configuration file. Default is
                        ~/.openstick
  -f FORMAT, --format FORMAT
                        Format to use for images.
  -j HOSTNAME, --hostname HOSTNAME
                        Hostname of the virtual machine.
  -i IMAGE, --image IMAGE
                        Virtual machine hard drive image path
  -m MEMORY, --memory MEMORY
                        Memory size of the virtual machine.
  -n NAME, --name NAME  Name of the virtual machine. Default is a random name.
  -p PORTS, --ports PORTS
                        Ports to forward.
  -r ROOT_IMAGE_PATH, --root ROOT_IMAGE_PATH
                        Path to a virtual machine image to use as root (base).
  -s SIZE, --size SIZE  Size of the virtual machine hard drive.
  -u SOCKETS, --sockets SOCKETS
                        Number of CPU sockets
  -t THREADS, --threads THREADS
                        Number of threads by core.

# ToDo
- Display VM configuration before startup
- Intelligent port generator
