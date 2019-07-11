#!-*- encoding: utf-8 -*-

import requests

linode_token = 'xxxx'


def get_interface_ipv6(interface):
    if_inet6 = open('/proc/net/if_inet6', 'r')
    for line in if_inet6.readlines():
        ip6 = line.split(' ')
        if ip6[-1].strip() == interface and not ip6[0].startswith('fe'):
            if_inet6.close()
            def ipv6_hex2char(seq):
                return ':'.join([seq[i:i+4] for i in range(0, len(seq), 4)])
            return ipv6_hex2char(ip6[0])
    if_inet6.close()


def update_dns_record(token, domain, subdomain, rec_type, value):
    headers = {'Authorization':  'Bearer ' + token}
    base_url = 'https://api.linode.com/v4'

    # get domain
    domains_url = base_url + '/domains'
    domains = requests.get(domains_url, headers=headers).json()
    domain = [i for i in domains['data'] if i['domain']==domain][0]

    # ger record
    records_url = base_url + '/domains/{domainId}/records'.format(domainId=domain['id'])
    records = requests.get(records_url, headers=headers).json()
    record = [i for i in records['data'] if i['name']==subdomain and i['type']==rec_type][0]

    # update record
    record['target'] = value
    record_id = record.pop('id')
    update_record_url = base_url + '/domains/{domainId}/records/{recordId}'.format(domainId=domain['id'], recordId=record_id)
    headers['Content-Type'] = 'application/json'
    result = requests.put(update_record_url, headers=headers, data=record)
    print(result.text)
    return True if result.status_code == 200 else False


ipv6_address = get_interface_ipv6('wlp2s0')
print(ipv6_address)
result = update_dns_record(linode_token, 'abc.com', 'www', 'AAAA', ipv6_address)
print(result)
