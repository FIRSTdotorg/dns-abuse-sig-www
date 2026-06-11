<!--
---
title: "DNS Abuse Detection: Domain name compromise"
...
-->

# DNS Abuse Detection: Domain name compromise

## Definition

*The wrongfully taking control of a domain name from the rightful name holder. Compromised domains can be used for different kinds of malicious activity like sending spam or phishing, for distributing malware or as botnet command and control.*

[https://www.icann.org/groups/ssac/documents/sac-007-en](https://www.icann.org/groups/ssac/documents/sac-007-en)

## Advice

Signs of domain compromise can be found in the DNS itself and by looking at the linked websites or resources: 

### Check DNS

A good starting point is to check domain name history and confirming what changes have occurred and when:

* Have NS records, A, or AAAA records for significant hostnames changed recently?

It also makes sense to investigate newly generated subdomains and check for changes as with the parent domain. If they’re being used for unusual or unrelated purposes, it might indicate a compromise. Also, monitor deviations such as:

* Subdomain records pointing to a different IP address  
* Subdomain records pointing to a different Autonomous System Networks (ASNs)

Compromises might also lead to other records. Therefore, check other record types \- for example, MX records might point to unrelated servers which are being used for malicious purposes, or TXT records might contain domain verification records from an attacker.

Look for DNSSEC failures on your resolver, as attackers without private keys may not be able to recreate signed DNS records. Querying your own domain on public resolvers might show failures.

When monitoring your own services, abrupt changes in latency or other anomalies might indicate services being routed incorrectly or fraudulently.

### Check related resources

Usually, domain name compromise does not happen in a vacuum. Take a look at the website for the domain for indicators of compromise:

* Content on the site should be clearly related to the domain  
* Check for certain patterns like a script injection or connections to unknown resources in the browser dev tool  
* Check for SSL certificate errors  
* Check if associated hosts or IPs are listed on relevant blocklists or otherwise suspicious

As before, compromise might be related to subdomains, so it makes sense to repeat above-mentioned steps for newly created subdomains in particular.

In case of domain compromise being related to email, also explore known blocklist providers and study relevant records, e.g. DKIM, DMARC. For example, have related records been removed or changed recently?

## Examples

Examples include domains which have been taken over for use in phishing and spam attacks, and domain shadowing attacks \- where admin control of a domain has been compromised, but existing DNS records are left alone and extra records are created for malicious use.

Reference \- [https://shreshtait.com/blog/2022/11/lk-domain-name/](https://shreshtait.com/blog/2022/11/lk-domain-name/) 

One possibility is changing the NS records for the parent zone to point towards nameservers until the attacker’s control.

Another would be compromising the account that controls the nameserver, or the system that controls the DNS records for the domain.

This happened with PCH during April 2019 where several international organizations had their records changed \- the registrar: [https://blog.talosintelligence.com/seaturtle/](https://blog.talosintelligence.com/seaturtle/), in particular figure 3\.

Some examples of detection techniques can be seen in this article by Shoko Nakai from June 2022: [https://blog.apnic.net/2022/06/30/investigating-dns-abuse-in-japan/](https://blog.apnic.net/2022/06/30/investigating-dns-abuse-in-japan/).

## Potential Resources

- Public facing websites related to the domains  
- Examples of emails used in phishing attacks, spams, etc. showing presumably unintended use  
- Passive DNS logs  
- If you are a registry, changes in NS are easy to detect and monitor  
- For Patterns to detect compromised domains: blogs, security researchers, X, mastodon  
- [Wayback Machine](https://wayback.archive.org/) for checking website history  
- Certificate Transparency (CT) logs \- monitoring CT logs can uncover subdomain names added in the parent if the threat actor requests for a TLS certificate.

## Related Advice

- [DNS server compromise](dns-server-compromise)
- [DNS Cache Poisoning](cache-poisoning)
- [Spoofing of a registered domain](spoofing-of-a-registered-domain)
- [Malicious registration of (effective) second level domains](malicious-registration-of-effective-second-level-domains)
