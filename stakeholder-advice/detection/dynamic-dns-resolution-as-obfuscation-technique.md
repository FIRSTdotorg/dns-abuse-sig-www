<!--
---
title: "DNS Abuse Detection: Dynamic DNS Resolution (as obfuscation technique)"
...
-->

# Dynamic DNS Resolution (as obfuscation technique)

### Definition

Dynamic DNS (DDNS) is a legitimate online service for many end users. However, because the IP addresses are dynamic and the DDNS services are free or relatively cheap, DDNS services are commonly used to enable other attacks such as phishing, fast-flux, or malware command and control.

Many online resources, such as file servers, APIs, or web servers, run on internet connections that have their IP addresses changed frequently. This creates a problem if the operators of those endpoints want to give a hosted resource a specific domain name. Dynamic DNS (DDNS) works by keeping the DNS updated with the correct IP address.

For example, if a web administrator is operating a website with a domain name of www.example.com and an IP address of 192.0.2.0, any time a user enters www.example.com into their browser, the DNS will direct them to the server at 192.0.2.0. If the server changes its IP address (e.g. if it was updated by the ISP), a dynamic DNS service can automatically update the DNS record to reflect this change.

(Adapted from: [https://www.cloudflare.com/en-gb/learning/dns/glossary/dynamic-dns/](https://www.cloudflare.com/en-gb/learning/dns/glossary/dynamic-dns/))

### Advice

There are several lists that can be found online of DDNS providers and their associated domains. Checking for these domains in your query logs or network logs can show whether they’re being used on your network or not.

Check for nameservers used by known DDNS providers and then look for domain names using those name servers.

Alternatively, the Public Suffix List, a list of all reported domain name suffixes that commonly have subdomains used for purposes other than their parent domains, could be used to identify new DDNS providers that might be used for DNS Abuse. Look for “dyn”, “ddns”, and similar keywords.

Domains that change their IP address frequently can indicate the use of a DDNS service, so checking for these in DNS query logs can also highlight their use. Passive DNS resources can be an asset here to identify domains that are doing this.

The support sections of major dynamic DNS service providers can often include official lists of the domains that they use.

### Examples

* [https://www.hyas.com/blog/the-prevalence-of-darkcomet-in-dynamic-dns](https://www.hyas.com/blog/the-prevalence-of-darkcomet-in-dynamic-dns)  
* [https://vercara.com/resources/dynamic-dns-resolution-as-an-obfuscation-technique\#elementor-toc\_\_heading-anchor-2](https://vercara.com/resources/dynamic-dns-resolution-as-an-obfuscation-technique#elementor-toc__heading-anchor-2) \- several examples included here

### Potential Resources

1. Known DDNS providers \- [https://github.com/korlabsio/subdomain\_providers](https://github.com/korlabsio/subdomain_providers)  
2. Another list \- [https://github.com/alexandrosmagos/dyn-dns-list](https://github.com/alexandrosmagos/dyn-dns-list)  
3. Public Suffix List \- [https://publicsuffix.org/list/public\_suffix\_list.dat](https://publicsuffix.org/list/public_suffix_list.dat)  
4. One example of a major provider’s domains \- [https://help.dyn.com/list-of-dyn-dns-pro-remote-access-domain-names/](https://help.dyn.com/list-of-dyn-dns-pro-remote-access-domain-names/)

