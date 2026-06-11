<!--
---
title: "DNS Abuse Detection: Lame delegations"
...
-->

# DNS Abuse Detection: Lame delegations

## Definition

*Lame delegations occur as a result of expired nameserver domains allowing attackers to take control of the domain resolution by re-registering this expired nameserver domain.*

[https://blog.apnic.net/2021/03/16/the-prevalence-persistence-perils-of-lame-nameservers/](https://blog.apnic.net/2021/03/16/the-prevalence-persistence-perils-of-lame-nameservers/).  
[https://kb.isc.org/docs/lame-servers-what-are-they-and-how-does-bind-deal-with-them, What are Lame Servers? (isc.org)](https://kb.isc.org/docs/lame-servers-what-are-they-and-how-does-bind-deal-with-them)

**Note:** these are also known as “dangling delegations”, which is the most common form of attack involving lame delegations. It’s also possible that lame delegations might help to enable [DoS attacks](dos-against-the-dns) or [compromises](domain-name-compromise), which are covered elsewhere.

## Advice

Tools that check the integrity of answers of the authoritative name service (e.g. [Zonemaster](https://github.com/zonemaster/zonemaster)) can help detect lame delegations.

Inspect domain delegations by querying authoritative nameservers.

Domain registries can automatically and regularly check the response from nameservers and report any errors to the domain holders.

Deploy DNSSEC to stop rogue nameservers taking over lame delegations. Do note however that this approach works only with DNSSEC validating resolvers.

## Examples

3 nameservers: one is not responding, or responding incorrectly. This is a lame delegation in the context of DNS Abuse.

## Potential Resources

- [https://www.apnic.net/manage-ip/manage-resources/reverse-dns/lame-dns-reverse-delegation/lame-delegation-test/](https://www.apnic.net/manage-ip/manage-resources/reverse-dns/lame-dns-reverse-delegation/lame-delegation-test/) \- Lame delegation test from APNIC  
- [https://dnsviz.net/](https://dnsviz.net/) for checking NS records (and much more)  
- [https://github.com/google/broken-dns](https://github.com/google/broken-dns) for checking lame delegation at scale

## See Also

- [DNS server compromise](dns-server-compromise)
- [Domain name compromise](domain-name-compromise)
- [DNS Cache Poisoning](cache-poisoning)
