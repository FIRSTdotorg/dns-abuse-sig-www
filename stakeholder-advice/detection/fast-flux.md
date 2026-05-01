<!--
---
title: "Fast Flux"
...
-->

# Fast flux

### Definition

DNS fast flux is a technique where the resource records of a domain are rapidly updated to avoid detection and takedown. "Double fast flux" is where both A/AAAA and NS records are updated to further hide malicious activity. Fast flux is used by botnets, command and control servers, to hide phishing sites, and generally to provide resilience to malicious resources.

Note: there are sometimes legitimate reasons for the use of fast flux, for example with CDNs or load balancers, but here we assume that the intent is malicious.

IP reputation can be affected by fast flux. As an example, when a fully qualified domain name (FQDN) using fast flux resolves to IP addresses of well-known service providers, the domain gains a positive reputation score and is less likely to be blocked by DNS firewalls or other filtering techniques.  The malware controllers can then temporarily resolve the FQDN to the IP address they use for their attack.

Fast flux is commonly used with other techniques such as CNAME chaining to create a malware distribution network or as a backup command and control (C2) server to regain control of their malware. Fast flux has some technical characteristics similar to valid DNS uses such as content distribution networks (CDNs) and other types of load balancing. However, there are certain technical features that are almost exclusively used in fast flux as opposed to similar benign use cases.

For example, fast flux networks use IP addresses on a variety of autonomous systems (AS) and effective second level domains whereas CDNs tend to own all the IP addresses they use, and therefore the IP addresses are in a small number of AS’s. Similarly, CDNs use a relatively small number of effective second level domains. Furthermore, the IP addresses in a CDN or load balancing setup are usually all active and not parked, whereas a fast flux network tends to use a large number of parked IP addresses. A parked domain is one on which no services are actually available on the target of the resource record.

### Advice

* Threat feed providers have lists of known fast-flux domains. These can be used proactively as a blocklist or retroactively to search logs for endpoints that have queried for these domains in the past.  
* Protective DNS services can help with detecting and blocking fast-flux domains because they can aggregate DNS query logs across a large number of endpoints.  
* DNS response patterns \- look for patterns where a single domain resolves to many different IPs in a short period of time.  
* Fast-flux DNS responses typically have unusually short TTL values.

### Examples

One of the first notable attacks using a “[domain-flux](https://en.wikipedia.org/wiki/Fast_flux#Double-flux_network)” network was the computer worm [Conficker](https://en.wikipedia.org/wiki/Conficker), first detected in late 2008\.

[Storm Worm Botnet](https://en.wikipedia.org/wiki/Storm_botnet) used fast flux as a resiliency technique also in 2008\.

Fast Flux remained a viable technique for Botnet resiliency through the 2010s, such as documented by Akamai in 2017:  
[https://www.akamai.com/newsroom/press-release/fast-flux-botnets-still-wreaking-havoc-on-internet-according-to-akamai-research](https://www.akamai.com/newsroom/press-release/fast-flux-botnets-still-wreaking-havoc-on-internet-according-to-akamai-research)

Another example from 2025 is the [GammaDrop Malware](https://thehackernews.com/2024/12/hackers-leveraging-cloudflare-tunnels.html) is first reported to use fast flux in December 2024\.

[Fast flux was labeled a “national security threat”](https://media.defense.gov/2025/Apr/02/2003681172/-1/-1/0/CSA-FAST-FLUX.PDF) by cybersecurity agencies from the USA, Canada, and Australia in 2025\.

### Potential Resources

Description of fast flux networks here: [Open-source Measurement of Fast-flux Networks While Considering Domain-name Parking | USENIX](https://www.usenix.org/conference/laser2017/presentation/metcalf) 

Detection via a network intrusion detection system:

* Associated open-source detection code available in [Analysis Pipeline](https://tools.netsa.cert.org/analysis-pipeline5/index.html)  
* Zeek dns.log \- [https://docs.zeek.org/en/master/logs/dns.html](https://docs.zeek.org/en/master/logs/dns.html)  
* Suricata [8.15. DNS Keywords — Suricata 8.0.0-dev documentation](https://docs.suricata.io/en/latest/rules/dns-keywords.html)

### Further reading

Fast Flux 101: How Cybercriminals Improve the Resilience of Their Infrastructure to Evade Detection and Law Enforcement Takedowns: [https://unit42.paloaltonetworks.com/fast-flux-101/](https://unit42.paloaltonetworks.com/fast-flux-101/)

The topic received attention and recommendations from the ICANN security and stability advisory committee for advice to the DNS community as early as March 2008\. 

* [https://itp.cdn.icann.org/en/files/security-and-stability-advisory-committee-ssac-reports/sac-025-en.pdf](https://itp.cdn.icann.org/en/files/security-and-stability-advisory-committee-ssac-reports/sac-025-en.pdf)  
* [https://ccnso.icann.org/files/atlarge/ssac-fast-flux-hosting-03sep08.pdf](https://ccnso.icann.org/files/atlarge/ssac-fast-flux-hosting-03sep08.pdf)  
* [https://media.blackhat.com/us-13/US-13-Xu-New-Trends-in-FastFlux-Networks-Slides.pdf](https://media.blackhat.com/us-13/US-13-Xu-New-Trends-in-FastFlux-Networks-Slides.pdf)  
  [https://www.researchgate.net/publication/350402517\_Research\_and\_Detection\_of\_Fast-flux\_Botnet](https://www.researchgate.net/publication/350402517_Research_and_Detection_of_Fast-flux_Botnet)

