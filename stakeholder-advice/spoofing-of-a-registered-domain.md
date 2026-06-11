<!--
---
title: "DNS Abuse Detection: Spoofing of a registered domain"
...
-->

# DNS Abuse Detection: Spoofing of a registered domain

## Definition

In contexts where a domain name is expected, such as in the "From" header of an email or in a URL within a webpage or message body, spoofing involves using a domain name that the attacker does not control, but which is actually owned or registered by a legitimate party.

This type of DNS abuse is related to, but distinct from, an [on-path attack](on-path-dns-attack) where a legitimate domain is being used but impersonated by modifying or spoofing DNS records.

## Advice

Since this type of issue manifests itself within the application layer, detecting it is dependent on the application in use. This means that detection depends on the application and specific context where it occurs.

One of the main examples is with email, where checking DMARC, and underlying SPF and DKIM, records by the receiving mailserver can indicate whether a domain is being spoofed. On the domain owner side, checking records being sent by an external receiving mailserver to an endpoint indicated in the DMARC records (“rua” and “ruf”) can help detect spoofing.

In other protocols and applications where registered domain names may be spoofed, similar mechanisms would need to be in place in order to enable detection.

For general purposes, to detect spoofing of a registered domain, defenders can compare legitimate locations where a domain can be used with other locations, such as in mail logs and web scans that may show unauthorised uses of a domain.

Cyber Threat Intelligence feeds can identify “repeat offenders” that often use spoofed domains, and can be used as a filter list to detect locations where domain spoofing is originating.

Certificate Authority certificate transparency logs can help to detect that a certificate was issued for a spoofed domain.

## Examples

One example is an attacker sending a phishing email, with the From address using “[example.com](http://example.com)” as the domain, when “[example.com](http://example.com)” is a domain registered by a legitimate owner.

Another example would be an attacker hiding a malicious domain in the address bar of a browser, or the content of an email, when a link actually goes to the malicious domain.

Malicious actors may also update hosts files to make legitimate domains go to malicious locations.

## Potential Resources

* [DMARC.org specifications](https://dmarc.org/resources/specification/)  
* [RFC 7489](https://datatracker.ietf.org/doc/html/rfc7489)  
* [Certificate Authority Transparency](https://certificate.transparency.dev/howctworks/)

## See Also

- [Use of an Unregistered Domain](use-of-an-unregistered-domain)
- [Malicious registration of (effective) second level domains](malicious-registration-of-effective-second-level-domains)
- [Domain name compromise](domain-name-compromise)
- [On-path DNS attack](on-path-dns-attack)
