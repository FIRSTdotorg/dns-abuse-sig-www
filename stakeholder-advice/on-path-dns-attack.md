<!--
---
title: "DNS Abuse Detection: On-path DNS attack"
...
-->

# DNS Abuse Detection: On-path DNS attack

## Definition

From [https://www.imperva.com/learn/application-security/dns-hijacking-redirection/](https://www.imperva.com/learn/application-security/dns-hijacking-redirection/\\):

“Attackers intercept communication between a user and a DNS server and manipulates the content of the reply to the client”

From [https://www.cloudflare.com/en-gb/learning/security/threats/on-path-attack/](https://www.cloudflare.com/en-gb/learning/security/threats/on-path-attack/): 

“On-path attackers place themselves between two devices (often a web browser and a web server) and intercept or modify communications between the two. The attackers can then collect information as well as impersonate either of the two agents. In addition to websites, these attacks can target email communications, DNS lookups, and public WiFi networks. Typical targets of on-path attackers include SaaS businesses, ecommerce businesses, and users of financial apps.”

On-path DNS attacks cover both manipulation of DNS queries and listening in on DNS traffic.

## Advice

To detect manipulation of DNS traffic, comparing DNSSEC-enabled queries against standard queries using local resolvers can highlight differences which might indicate an on-path attack. In general, DNSSEC signed resource records should be validated, and if the validation fails, the answer should be considered to be manipulated.

Another possibility is to check SSL certificates on websites to see that they are verified accurately.

However, it can be hard or impossible to detect whether an on-path attack which is simply sniffing traffic is happening. This is because if traffic is being listened to, there can be no external indications at all that this is taking place.

Comparing DNS query results against IP address reputation lists can potentially indicate that a query reply has been manipulated.

## Examples

### **The Great Firewall**

[The Great Firewall](https://en.wikipedia.org/wiki/Great_Firewall), part of China’s [Golden Shield Project](https://en.wikipedia.org/wiki/Golden_Shield_Project) sometimes adds responses to DNS traffic that are sent to the client before other responses. A recent example of such an attack is the “[Muddling Meerkat](https://www.bleepingcomputer.com/news/security/muddling-meerkat-hackers-manipulate-dns-using-chinas-great-firewall/)” actor manipulating MX records.

### **NSA QUANTUM toolset**

From the Snowden leaks we know that NSA has the capability to perform similar attacks as part of the [QUANTUM](https://www.wired.com/2014/03/quantum/) toolset.

## Potential Resources

- DNS query logs can show historical responses from DNS servers, for comparison against live responses with DNSSEC-enabled servers  
- SSL certificate details from browsers can be examined  
- IP reputation lists can be used to potentially highlight manipulated results, if a query reply includes an IP that has been flagged as malicious unexpectedly

## Related Advice

- [DNS Cache Poisoning](cache-poisoning)
- [Local recursive resolver hijacking](local-resolver-hijacking)
- [Stub resolver hijacking](stub-resolver-hijacking)
- [Spoofing of a registered domain](spoofing-of-a-registered-domain)
