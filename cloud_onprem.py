#!/usr/bin/env python2
## Mandatory imports
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

## Optional imports
from cms_wrapper import CMSWrapper
import sys
import argparse
import os
from datetime import datetime

## Script definitions
cloud_none={'is_cloud':'None', 'hostname': []}
cloud_yes={'is_cloud':'Yes', 'hostname': []}
filepath_none="/tmp/hosts_cloud_None"
filepath_yes="/tmp/hosts_cloud_Yes"

def get_arguments():
    parser = argparse.ArgumentParser(description="Separate cloud and on-prem servers.\n", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--file", type=str.lower, help="File having host names")

    if len(sys.argv) <= 2:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    return args

def get_hostlist(filename):
    # Read hostlist from file.
    with open(filename,'r') as f:
        hostnames = f.readlines()
        hostnames_ = [host.strip() for host in hostnames]
        hostnames__ = []
        for i in hostnames_:
            if not i.strip():
                continue
            if i:
                hostnames__.append(i)
    return hostnames__

def is_cloud_data():
    '''
    Returns server information. Ex:
    {u'vmkiwi': {u'is_cloud': None, u'hostname': u'vmkiwi', u'country_code': u'LU', u'env': None}}
    We are checking is_cloud key: None or X
    '''
    host_list = get_hostlist(args.file)
    host_unreachable = []
    for hostnm in host_list:
        output=a.get_cms_data(filter={'hostname': [hostnm]},columns=['hostname','is_cloud'])
        if bool(output) == False:
            host_unreachable.append(hostnm)
        else:
            host_data = output[hostnm]

        if host_data['is_cloud'] == None:
            cloud_none['hostname'].append(host_data['hostname'])
        if host_data['is_cloud'] == 'X':
            cloud_yes['hostname'].append(host_data['hostname'])

    return cloud_none, cloud_yes, host_unreachable

def write_file(is_cloud,data):
    '''
    :is cloud: Yes|None, value for file name
    '''
    if is_cloud == 'None':
        with open(filepath_none,'a+') as f:
            f.write(data+'\n')
    if is_cloud == 'Yes':
        with open(filepath_yes,'a+') as f:
            f.write(data+'\n')

def main():
    # Main script
    output=is_cloud_data()
    if os.path.exists(filepath_none):
        os.remove(filepath_none)
    if os.path.exists(filepath_yes):
        os.remove(filepath_yes)

    try:
        for h_none in set(output[0]['hostname']):
            write_file('None',h_none)

        for h_yes in set(output[1]['hostname']):
            write_file('Yes',h_yes)
    except:
        print("There is an error.\nPlease check the code or host reachability.\n")
    print("Files under: ", filepath_none,'-',filepath_yes)
    print("Following hosts are unreachable or not found in CMS:", output[2])

if __name__=='__main__':
    starttime = datetime.now()
    args=get_arguments()
    a=CMSWrapper()
    main()
    print(datetime.now() - starttime)
