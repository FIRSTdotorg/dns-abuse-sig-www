<!--
---
title: "DNS Abuse Detection: Cache Poisoning"
...
-->

# DNS Abuse Detection: Cache Poisoning

## Definition

DNS cache poisoning – also known as DNS spoofing – is a type of cyber attack in which an  
attacker corrupts a DNS resolver's cache by injecting false DNS records, causing the resolver  
to return incorrect responses that are controlled by the attacker \- usually for redirecting users or machines to malicious resources like phishing pages or attacker-controlled proxies.

CAPEC entry: [https://capec.mitre.org/data/definitions/142.html](https://capec.mitre.org/data/definitions/142.html)

Some examples of how this can be achieved by the attacker are through on-path modification of network traffic, sending false updates to improperly secured caching DNS servers, or exploiting vulnerabilities in implementations or protocols.

## Advice

DNSSEC validation can be used to detect whether cache poisoning has been attempted. Checking logs for validation failures can highlight potential incidents, but it should be noted that these failures may be due to incorrectly configured domains.

It can be hard to confirm the intent, as an incorrect cache result may be just a mistake.

To confirm whether a DNS cache is returning incorrect results, you can compare the results from a DNS cache to that of the authoritative server \- however, to be completely sure, DNSSEC validation must be on for the query to the authoritative server.

So, the following conditions must be met:

* DNSSEC validation must be enabled  
* A query to the authoritative server must fail to match that of the cache being queried

One other technique is randomisation of domains in the DNS queries, to determine whether a fake result is being injected. This requires the 0x20 bit to be set in the initial query. A description of this technique can be found here:

[https://www.theregister.com/2023/01/19/google\_dns\_queries/](https://www.theregister.com/2023/01/19/google_dns_queries/)

And an internet draft covering this from 2008 can be found here:

[https://datatracker.ietf.org/doc/html/draft-vixie-dnsext-dns0x20-00](https://datatracker.ietf.org/doc/html/draft-vixie-dnsext-dns0x20-00)

For DNS cache poisoning, a compromise of any upstream server would also lead to cache poisoning downstream, if the downstream server were to request the affected records while they are inaccurate. Cache poisoning can take considerable amounts of time until poisoned records are flushed post detection. 

## Examples

### DNSpionage / SeaTurtle

[https://www.netfort.com/blog/dnspionage-dns-server-hijacking-attack/](https://www.netfort.com/blog/dnspionage-dns-server-hijacking-attack/)  
[https://krebsonsecurity.com/tag/dnspionage/](https://krebsonsecurity.com/tag/dnspionage/)

### MyEthereumWallet

Route53 BGP attack, attackers pretended to be Route53 authoritative servers  
[https://techcrunch.com/2018/04/24/myetherwallet-hit-by-dns-attack/](https://techcrunch.com/2018/04/24/myetherwallet-hit-by-dns-attack/)

### uLibC vulnerability

[https://thehackernews.com/2022/05/unpatched-dns-related-vulnerability.html](https://thehackernews.com/2022/05/unpatched-dns-related-vulnerability.html)

### MaginotDNS attack

[https://www.bleepingcomputer.com/news/security/maginotdns-attacks-exploit-weak-checks-for-dns-cache-poisoning/](https://www.bleepingcomputer.com/news/security/maginotdns-attacks-exploit-weak-checks-for-dns-cache-poisoning/)

## Potential Resources

- DNSSEC validation logs  
- [https://www.internetsociety.org/deploy360/dnssec/tools/](https://www.internetsociety.org/deploy360/dnssec/tools/)

