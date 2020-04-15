#! /usr/bin/env python3

import requests as http
import json

# DNSPOD API ID
ID = '00000'
# DNSPOD API TOKEN
TOKEN = 'xxxxxxxxxxxxxxxxxxxx'
LOGIN_TOKEN = ID + ',' + TOKEN
# YOUR DOMAIN ID
DOMAINID = '11111111'
# you want to update sub domains
sub_domains = ['www', 'blog', '@', '*']
update_domains = []


def get_public_ip():
    res = http.get('https://api.ip.sb/ip')
    return res.text.rstrip("\n\r")


def get_domain_list():
    url = 'https://dnsapi.cn/Domain.List'
    res = http.post(url, {"login_token": LOGIN_TOKEN, "format": "json"})
    jsonRes = res.json()
    domains = jsonRes['domains']
    for domain in domains:
        print("Domain Id:{},Domain Status:{},Domain:{}".format(domain['id'], domain['status'], domain['punycode']))


def update_dnspod_multi(ip):
    url = 'https://dnsapi.cn/Record.Modify'
    for record in update_domains:
        sub_domain = record['name']
        record_type = 'A'
        record_line = '默认'
        value = ip
        record_id = record['id']
        res = http.post(url, {
            "login_token": LOGIN_TOKEN,
            "format": "json",
            "domain_id": DOMAINID,
            "record_id": record_id,
            "sub_domain": sub_domain,
            "record_type": record_type,
            "record_line": record_line,
            "value": value
        }, headers={"UserAgent": "Python3-requests/release(whatuwant)"})
        # print(res.json())
    print("Action Completed")


def get_domain_records(domain):
    url = 'https://dnsapi.cn/Record.List'
    res = http.post(url, {
        "login_token": LOGIN_TOKEN,
        "format": "json",
        "domain": domain
    })
    records = res.json()
    records = records['records']
    for record in records:
        if record['name'] in sub_domains:
            update_domains.append(record)


def main():
    ip = get_public_ip()
    get_domain_records('yourdomain.com')
    update_dnspod_multi(ip)


if __name__ == "__main__":
    main()
