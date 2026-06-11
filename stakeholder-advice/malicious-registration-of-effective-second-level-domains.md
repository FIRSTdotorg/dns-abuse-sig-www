<!--
---
title: "DNS Abuse Detection: Malicious registration of (effective) second level domains"
...
--->
# DNS Abuse Detection: Malicious registration of (effective) second level domains

## Definition

Malicious registration of domains is the creation of new domains by threat actors online.

This technique is when someone who is going to do a bad thing registers a domain themselves. It is distinguished from an actor stealing, compromising, taking over, or otherwise hijacking DNS resources.

## Advice

Malicious registration is about the intent of how the domain will be used after it is registered. While it is impossible to predict with 100% accuracy who is registering a domain for malicious purposes, registrars and registries have signals that can be used as indicators for future malicious intent.

Registries and registrars are the only stakeholders able to detect malicious domains before or at the time of registration since they are the only ones who have insight in the relevant data at this time. Registrars have the most information to correlate with potential malicious use, followed by registries, and then everyone else. Public information on registration data has decreased since ICANN restricted the public WHOIS. However, registries can correlate registrant activity across registrars; therefore, a large registry can gather this information widely in a way that many registrars cannot. 

Registries and registrars can use this data to check for things like:

* Stolen credit cards  
* Fraudulent addresses and stolen identities or any inconsistencies ins customer data  
* Standard Know Your Customer (KYC) techniques used to detect criminal activity  
* History of abuse reports against a registrant

Higher registration fee is correlated with fewer malicious domain registrations. Fees raise the cost for the attackers, who are assessing return on investment. 

When a domain is reported to the registry/registrar as malicious, the registrar should check other domains owned by the registrant to determine if they also are malicious.

After registration, other stakeholders can look for signals to detect malicious intent, such as:

* History of abuse or complaints against the registrant  
* The registrant’s domain registration history  
* Signs of [typosquatting](https://capec.mitre.org/data/definitions/630.html)  
* Known malicious infrastructure  
* Use of known [bulletproof hosting](https://en.wikipedia.org/wiki/Bulletproof_hosting) providers  
* Registration IP address geo-ip   
* IP address reputation, including history of blocklists mentioning the IP  
* How long ago the domain was registered

These lists are illustrative and are not exhaustive.

When a domain is reported as malicious, it should be put on blocklists enforced at the recursive/resolver level. Blocklist information can be shared via cyber threat intelligence channels.

One of the primary purposes of protective DNS is to ingest blocklists and domain information and perform correlations to determine domain reputation scores across indicators of compromise. Protective DNS then will block malicious domains as they are detected.

## Examples

MITRE’s entry for “Acquire Infrastructure: Domains” has a [good list of examples](https://attack.mitre.org/techniques/T1583/001/#examples) with links to external reports.

## Potential Resources

* [Palo Alto page on “What Are Malicious Newly Registered Domains?”](https://www.paloaltonetworks.co.uk/cyberpedia/what-are-malicious-newly-registered-domains)  
* [A M3AAWG Introduction to Addressing Malicious Domain Registrations](https://www.m3aawg.org/sites/default/files/m3aawg-maliciousdomainregistratinos-2018-06.pdf)  
* [MITRE entry for “Acquire Infrastructure: Domains”](https://attack.mitre.org/techniques/T1583/001/)  
* [Newly Registered Domains blocklist](https://github.com/xRuffKez/NRD)

## See Also

- [DGA domains](dga)
- [Creation of Malicious Subdomains Under Dynamic DNS Providers](creation-of-malicious-subdomains-under-dynamic-dns-providers)
- [Spoofing of a registered domain](spoofing-of-a-registered-domain)
- [Fast flux](fast-flux)
