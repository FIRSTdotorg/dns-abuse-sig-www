<!--
---
title: "DNS Abuse Detection: DNS Beacons - C2 Communication"
...
-->
# DNS Beacons - C2 Communication

## Definition

Some kinds of malware send periodic DNS queries to command and control (C2) servers. These periodic communications are known as beacons. DNS beacons can be used to re-establish control over malware, as a form of keepalive for infected hosts, or a low-bandwidth form of C2 communication.

## Advice

Because beaconing is infrequent, it can make it harder to detect.

Configure the environment to only use authorized DNS resolvers, and check for outbound DNS traffic. This may implicate DNS beacons being attempted. The query logs on the configured resolvers can also be used to detect known C2 domains.

Check for network traffic to known malicious DNS servers in environments where any outbound DNS queries are allowed.

Examine regular DNS queries for known patterns of DNS beacons.

Reverse engineer malware to discover beaconing domains.

C2 beaconing frequently combines techniques such as [DNS fast-flux](fast-flux), [DGA domains](dga), and [DNS tunneling](dns-tunneling). See advice on those techniques for more information.

## Examples

[APT39, ITG07, Chafer, Remix Kitten, Group G0087 | MITRE ATT&CK®](https://attack.mitre.org/groups/G0087/)

[Cobalt Strike](https://www.cobaltstrike.com/product/features/beacon) explicitly details beacons as a product feature.

The [ZLoader Malware released an update](https://thehackernews.com/2024/12/zloader-malware-returns-with-dns.html) which added C2 communications over DNS.

[SUNBURST used DNS for C2 communications](https://cloud.google.com/blog/topics/threat-intelligence/sunburst-additional-technical-details).

## Potential Resources

DNS query logs on authorized resolvers can be used for the purposes detailed above. Protective DNS in particular can be used to find malicious domains being queried as C2 beacons.

[CISA wrote a really good guide on implementing enterprise DNS](https://www.cisa.gov/sites/default/files/2024-05/Encrypted%20DNS%20Implementation%20Guidance_508c.pdf) in order to detect and block DNS beaconing and C2. 

Netskope has a white paper on [detecting C2 beaconing](https://www.netskope.com/resources/white-papers/effective-c2-beaconing-detection-white-paper).  

## See Also

- [DGA domains](dga)
- [Fast flux](fast-flux)
- [DNS tunneling](dns-tunneling)
- [Infiltration and exfiltration via the DNS](infiltration-and-exfiltration-via-the-dns)
