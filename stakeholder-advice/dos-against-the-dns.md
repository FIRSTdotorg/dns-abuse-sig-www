<!--
---
title: "DNS Abuse Detection: DoS Against the DoS"
...
-->
# DNS Abuse Detection: DoS Against the DoS

## Definition

DoS stands for Denial of Service. A DoS attack against the DNS aims to ultimately result in the DNS service becoming inaccessible or severely degraded. DoS attacks may be crashing a DNS server via some form of vulnerability in the DNS server software or cutting off access through a network interruption.

In Distributed Denial of Service (DDoS) attacks, attackers deploy multiple devices to attack a single DNS server, depleting its network, memory, and CPU resources.

## Advice

One indicator of a DoS attack can be a sudden surge in network traffic and DNS query volume that exceeds normal levels. Also, a surge in the ANY request type can be an indicator. 

Unexplained crashes on the DNS server itself, severely increased resource usage, or unresponsive DNS servers can also indicate a DoS attack.

To detect this, use an availability monitoring system or IDS/IPS to check if the servers are still functioning as intended and to check traffic for anomalies and irregularities. [Snort](https://www.snort.org/), [Zeek](https://zeek.org/), and [Suricata](https://suricata.io/), are examples of open source IDS tools to deploy for this function.

Analyze traffic logs to identify high numbers of multiple requests from a single IP address, especially within a short period of time.

Investigation of the DNS server system logs and resource usage for evidence of unexplained crashes. If the authoritative DNS server is outsourced, it may not be possible to obtain logs or other information, making it difficult to notice anything unusual.

**To check if your authoritative DNS is working:**

- Check if a target domain can be resolved by querying the authoritative server directly.

- To do this, check the WHOIS data, or use the NS records for a domain, find the authoritative nameservers, and then specify the target NS server to resolve the domain name. Then check if the correct DNS records are returned.

- If an availability monitoring service is being used for authoritative DNS, log in and check the current status.

**To check if your DNS resolver is working:**

- Provided you have access to the resolver that you want to check, query it, and see if a response is provided.

- If no result is returned, that may be an indication that the resolver is under a DoS attack.

## Examples

### Mirai Malware attack (DDoS)

[https://www.cloudflare.com/en-gb/learning/ddos/glossary/mirai-botnet/](https://www.cloudflare.com/en-gb/learning/ddos/glossary/mirai-botnet/)

[https://en.wikipedia.org/wiki/Mirai\_(malware)\#Use\_in\_DDoS\_attacks](https://en.wikipedia.org/wiki/Mirai_\(malware\)#Use_in_DDoS_attacks) 

[https://en.wikipedia.org/wiki/DDoS\_attacks\_on\_Dyn](https://en.wikipedia.org/wiki/DDoS_attacks_on_Dyn)

### KeyTrap (Vulnerability)

[https://www.athene-center.de/en/keytrap](https://www.athene-center.de/en/keytrap)

### DNS Water Torture a/ Pseudo Random Subdomain attack / NXDOMAIN attack

[https://vercara.com/resources/whats-this-nxdomain-dns-query-response-and-why-do-i-have-them](https://vercara.com/resources/whats-this-nxdomain-dns-query-response-and-why-do-i-have-them)

## Potential Resources

- DNS and website availability monitoring services can help improve overall visibility of potential DoS attacks  
- Network monitoring with netflow, SNMP, MRTG, etc. can also help here  
- DNS query logs and DNS server system logs can be used for manual checking, or fed into systems to identify DoS attacks, particularly in cases of application vulnerabilities  
- Gather information on what kind of attacks are being launched against DNS currently through community channels  
- In case of outsourced DNS, check with your provider to see what resources or information they might have

## Related Advice

- [DNS as a vector for DoS](dns-as-a-vector-for-dos)
- [Use of an Unregistered Domain](use-of-an-unregistered-domain)
- [Lame delegations](lame-delegations)
