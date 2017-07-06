#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Copyright 2017 Julien Girard 
#
#    Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3 ;
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://http://www.gnu.org/licenses/gpl-3.0.html
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

import argparse
import configparser
import names
import os
import socket

def get_open_port():
    """
    http://stackoverflow.com/questions/2838244/get-open-tcp-port-in-python/2838309#2838309
    :return: free port
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def is_open_port(port):
    p = int(port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Test if port is open
            s.bind(("", p))
            is_open = p
        except socket.error as e:
            # If port is use, we try with next port
            if e.errno == 98:
                is_open = is_open_port(p + 1)
            else:
                print(e)
        except OverflowError as e:
            # If port is overflow, we get a random open port
            is_open = get_open_port()
    return is_open


def get_fw_port(port):
    if ":" in port:
        fw_port = is_open_port(port.split(":")[-1])
    else:
        fw_port = get_open_port()
    return fw_port


def launch():
    # Parse command line arguments.
    parser = argparse.ArgumentParser(description='Because sometimes you don\'t need a full stack')

    parser.add_argument(
        '-b', '--boot',
        help='Boot option. Can be hdd, cdrom or network.',
        dest='boot'
    )
    parser.add_argument(
        '-c', '--cores',
        help='Number of cores for the virtual machine.',
        dest='cores'
    )
    parser.add_argument(
        '-d', '--disk',
        help='Path to a disk image',
        dest='disk'
    )
    parser.add_argument(
        '-e', '--domains',
        help='DNS to look for.',
        dest='domains'
    )
    parser.add_argument(
        '--file',
        help='Path to the configuration file. Default is ~/.openstick',
        dest='configuration_file_path',
        default=os.path.expanduser('~') + '/.openstick'
    )
    parser.add_argument(
        '-f', '--format',
        help='Format to use for images.',
        dest='format'
    )
    parser.add_argument(
        '-j', '--hostname',
        help='Hostname of the virtual machine.',
        dest='hostname'
    )
    parser.add_argument(
        '-i', '--image',
        help='Virtual machine hard drive image path',
        dest='image'
    )
    parser.add_argument(
        '-m', '--memory',
        help='Memory size of the virtual machine.',
        dest='memory'
    )
    parser.add_argument(
        '-n', '--name',
        help='Name of the virtual machine. Default is a random name.',
        dest='name',
        default=names.get_first_name()
    )
    parser.add_argument(
        '-p', '--ports',
        help='Ports to forward.',
        dest='ports'
    )
    parser.add_argument(
        '-r', '--root',
        help='Path to a virtual machine image to use as root (base).',
        dest='root_image_path'
    )
    parser.add_argument(
        '-s', '--size',
        help='Size of the virtual machine hard drive.',
        dest='size'
    )
    parser.add_argument(
        '-u', '--sockets',
        help='Number of CPU sockets',
        dest='sockets'
    )
    parser.add_argument(
        '-t', '--threads',
        help='Number of threads by core.',
        dest='threads'
    )

    args = parser.parse_args()

    # Parse configuration file.
    config = configparser.ConfigParser()
    config.read(args.configuration_file_path)

    # Write specified values to configuration file.
    vm_name = args.name.lower()

    if not vm_name in config:
        config[vm_name] = {}

    exclude_args = ["configuration_file_path"]

    for key, value in vars(args).items():
        if key in exclude_args or value is None:
            continue
        config[vm_name][key] = value

    with open(args.configuration_file_path, 'w') as configfile:
        config.write(configfile)

    # Initialize Parameters.
    vm_boot = config.get(vm_name, 'boot', fallback='hdd')
    vm_cores = config.get(vm_name, 'cores', fallback='2')
    vm_disk = config.get(vm_name, 'disk', fallback='/dev/null')
    vm_domains = config.get(vm_name, 'domains', fallback='')
    vm_hostname = config.get(vm_name, 'hostname', fallback='%s-%s-%s' % (socket.gethostname(), os.getlogin(), vm_name))
    vm_format = config.get(vm_name, 'format', fallback='qcow2')
    vm_image = os.path.expanduser(
        config.get(vm_name, 'image', fallback=os.path.join(os.path.expanduser('~/VMs'), '%s.%s' % (vm_name, vm_format)))
    )
    vm_memory = config.get(vm_name, 'memory', fallback='1G')
    vm_ports = config.get(vm_name, 'ports', fallback='22,80,443')
    vm_size = config.get(vm_name, 'size', fallback='20G')
    vm_sockets = config.get(vm_name, 'sockets', fallback='1')
    vm_threads = config.get(vm_name, 'threads', fallback='1')

    # Create the base directory of the vm_image if necessary
    vm_image_dir = os.path.dirname(vm_image)
    if not os.path.isdir(vm_image_dir):
        os.makedirs(vm_image_dir)

    # Create virtual machine image if it does not exist.
    if not os.path.isfile(vm_image):
        if args.root_image_path is not None:
            os.system('qemu-img create -f %s -b %s %s' % (vm_format, args.root_image_path, vm_image))
        else:
            if vm_boot != 'cdrom' and vm_boot != 'network':
                print('You\'re trying to create a new virtual machine but does not specify boot from cdrom or network.')
                exit(1)
            else:
                os.system('qemu-img create -f %s %s %s' % (vm_format, vm_image, vm_size))

    # Build network configuration
    vm_network = 'user,id=net0,hostname=%s' % vm_hostname
    for domain in [x for x in vm_domains.split(',') if x]:
        vm_network = '%s,dnssearch=%s' % (vm_network, domain)

    print("VM name is : %s" % vm_name)

    # Forward port
    for port in [x for x in vm_ports.split(',') if x]:
        fw_port = get_fw_port(port)
        if ":" in port:
            port = port.split(":")[0]
        else:
            pass
        print("Forward port %s to : %s" % (port, fw_port))
        vm_network = '%s,hostfwd=tcp::%s-:%s' % (vm_network, fw_port, port)

    # Build boot option
    if vm_boot == 'hdd':
        vm_boot_option = 'c'
    elif vm_boot == 'cdrom':
        vm_boot_option = 'd'
    elif vm_boot == 'network':
        vm_boot_option = 'n'
    else:
        print('Invalid boot option: \'%s\'' % vm_boot)
        exit(2)

    # Start virtual machine.
    os.system('qemu-system-x86_64 -enable-kvm -smp cores=%s,threads=%s,sockets=%s -hda %s -device virtio-net-pci,netdev=net0,id=nic0 -netdev %s -m %s -boot %s -cdrom %s -monitor stdio' % (
        vm_cores,
        vm_threads,
        vm_sockets,
        vm_image,
        vm_network,
        vm_memory,
        vm_boot_option,
        vm_disk
    ))


def list():
    # Parse command line arguments.
    parser = argparse.ArgumentParser(description='Because sometimes you don\'t need a full stack')

    parser.add_argument(
        '--file',
        help='Path to the configuration file. Default is ~/.openstick',
        dest='configuration_file_path',
        default=os.path.expanduser('~') + '/.openstick'
    )

    args = parser.parse_args()

    # Parse configuration file.
    config = configparser.ConfigParser()
    config.read(args.configuration_file_path)

    for name in config.sections():
        print(name)


# Launch main if call as a script
if __name__ == '__main__':
    launch()
