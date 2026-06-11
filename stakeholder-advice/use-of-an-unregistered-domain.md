<!--
---
title: "DNS Abuse Detection: Use of an Unregistered Domain"
...
-->
# DNS Abuse Detection: Spoofing or otherwise using unregistered domain names

## Definition

This is the use of a domain in a context where a domain name is expected (such as the From header in mail or a URL in a web page or message body), and providing an unregistered domain name.

An unregistered domain in this context is any domain which does not exist in the DNS. Registrars can “register” a domain, but still not publish it in the parent registry, however it is effectively the same.

It should be noted that use of an unregistered domain is not always technically “DNS Abuse”. However, due to this technique’s relation to and interaction with the DNS, it is considered useful to include advice as a category to aid incident responders and security teams in their work.

Abuse of this type also includes deliberately invalid queries to a DNS server to generate NXDOMAIN responses. This is also known as a “[water torture attack](dos-against-the-dns)”, where resources are expended as part of an attack. NSEC3 exacerbates this due to the increased resources needed for generating hashes.

Another use of unregistered domains is with [DGA](dga), where a piece of malware may generate a list of thousands of domains which are potentially their Command and Control server, but only one or a few are actually registered.

## Advice

The potential for abuse by borrowing legitimacy of a potential domain name is higher in some contexts than others. These are generally where an actor can enter arbitrary text but it is not obvious to the receiver the text is arbitrary rather than a registered domain name.

One prominent situation in which this can be abused is the “From:” fields in email. The Domain-based Message Authentication, Reporting, and Conformance ([DMARC](https://en.wikipedia.org/wiki/DMARC)) protocol specifies a method whereby domain owners and mail receivers can collaborate to detect and optionally reject mail that spoofs a domain registered to the domain owner (see [Spoofing of a registered domain](spoofing-of-a-registered-domain)).

However, DMARC does not directly prevent use of unregistered domains without enforcing. While a mail server may not be able to prevent an actor from using an unregistered domain in a “From:” field, they can check to see whether any domains in such a field are registered by querying the DNS for the name.

In the case of unregistered domains being used in phishing or other fraudulent content, unregistered domains can be detected by querying the domain and checking for an NX response. However, this is not a usual process to happen while rendering HTML.

## Examples

Registries can receive abuse notifications of unregistered domains when they have been used in phishing attacks, and in emails.

Phishing websites may use unregistered domains to appear legitimate.

Malware may try to hide legitimate C2 domains inside a collection of unregistered domains.

## Potential Resources

DNS query logs showing NX responses.  

## See Also

- [Spoofing of a registered domain](spoofing-of-a-registered-domain)
- [DGA domains](dga)
- [DoS Against the DNS](dos-against-the-dns)
- [DNS as a vector for DoS](dns-as-a-vector-for-dos)
