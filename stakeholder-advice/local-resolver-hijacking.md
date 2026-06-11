<!--
---
title: "DNS Abuse Detection: Local recursive resolver hijacking"
...
-->

# DNS Abuse Detection: Local recursive resolver hijacking

## Definition

Consumer Premise Equipment (CPE), such as home routers, often provide DNS recursion on the local network. If the CPE device is compromised, the attacker can change the recursive resolver behavior; for example, by changing responses.

In a corporate environment, this may be a DNS resolver configured on a local network.

## Advice

Monitor anomalous DNS traffic, most specifically where the responses are NXDOMAIN. The recursive resolver can be configured by enabling Extended errors (RFC 8914 \- [https://www.rfc-editor.org/rfc/rfc8914](https://www.rfc-editor.org/rfc/rfc8914)).

Compare local DNS lookup results with results from directly querying a public resolver such as Quad9 (9.9.9.9) or Google DNS (8.8.8.8). Different results may indicate a local [server compromise](dns-server-compromise).

If possible, check the local resolver for indications of system compromise.

Configuring DNS over HTTPS in a browser and comparing views may also show indications of a local resolver hijack.

## Examples

### DNS Hijacking Attacks on Home Routers in Brazil

[https://cujo.com/blog/dns-hijacking-attacks-on-home-routers-in-brazil/](https://cujo.com/blog/dns-hijacking-attacks-on-home-routers-in-brazil/)

### Thousands of vulnerable TP-Link routers at risk of remote hijack

[https://techcrunch.com/2019/05/22/tp-link-routers-vulnerable-remote-hijack/](https://techcrunch.com/2019/05/22/tp-link-routers-vulnerable-remote-hijack/)

## Related Advice

- [Stub resolver hijacking](stub-resolver-hijacking)
- [On-path DNS attack](on-path-dns-attack)
- [DNS Cache Poisoning](cache-poisoning)
- [DNS server compromise](dns-server-compromise)
