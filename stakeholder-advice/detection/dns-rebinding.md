<!--
---
title: "DNS Abuse Detection: DNS rebinding"
...
-->

# DNS Abuse Detection: DNS rebinding

## Definition

DNS rebinding is a type of attack where a malicious website directs a client to a local network  
address, allowing the attacker to bypass the same-origin policy and gain access to the victim's  
local resources. \- [https://capec.mitre.org/data/definitions/275.html](https://capec.mitre.org/data/definitions/275.html)

## Advice

Monitor domain names which have a low TTL value. In order to do this, DNS telemetry would need to be collected in a passive manner using something like **dnstap** ([https://dnstap.info/](https://dnstap.info/)) or **Zeek** ([https://zeek.org/](https://zeek.org/)).

It is also important to take into account false positives \- i.e a large number of legitimate domain names are configured with a low TTL value. 

Another method to detect DNS rebinding is to use DNS Response Policy Zones (RPZ) and log/block domain names pointing at RFC1918/private address space. 

Specifically, by using Response IP Address Policy Trigger ([https://datatracker.ietf.org/doc/html/draft-ietf-dnsop-dns-rpz-00\#section-4.3](https://datatracker.ietf.org/doc/html/draft-ietf-dnsop-dns-rpz-00#section-4.3)) in a recursive resolver and a corresponding zone file containing a list of RFC1918/private address space.

## Examples

### SpaceX Wi-Fi Router Vulnerability

[https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-52235](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-52235)  
SpaceX Starlink Wi-Fi router GEN 2 before 2023.53.0 and Starlink Dish before 07dd2798-ff15-4722-a9ee-de28928aed34 allow CSRF (e.g., for a reboot) via a DNS Rebinding attack.

### Omise.co

[https://hackerone.com/reports/1379656](https://hackerone.com/reports/1379656)