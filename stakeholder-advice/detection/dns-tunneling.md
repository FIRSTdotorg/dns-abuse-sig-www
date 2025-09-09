<!--
---
title: "DNS Abuse Detection: DNS Tunneling - Tunneling Another Protocol Over DNS"
...
-->

# DNS Abuse Detection: DNS tunneling \- tunneling another protocol over DNS

### Definition

DNS tunneling is the use of the DNS network protocols to encapsulate other protocols. Tunneling is a process in which the client encodes and sends requests and responses to a server that accepts DNS requests, which will translate or decode the DNS traffic and convert it to the target protocol. DNS tunneling can be used for command and control (“C2” or” C\&C”) communication and as a functional equivalent of a Virtual Private Network.

DNS tunneling could be used for [exfiltration and infiltration](https://docs.google.com/document/d/1AZLd0yoi_JATRyVxsIfwPh3_I-UKnJtVkAbfZGcJhhw/edit?tab=t.0#heading=h.foa9ka5fpexn). Exfiltration and infiltration of information via the DNS has been separated into another section in order to address the different approaches in detection and prevention.

### Advice

The monitoring infrastructure to detect DNS tunneling requires careful consideration. Detection can be challenging by just looking at the queries since DNS tunneling uses the DNS protocol. Without context, the use of DNS may appear to be a normal client sending DNS requests to a remote server, and receiving responses as normal. Use of encrypted DNS protocols such as DNS-over-TLS (DoT) or DNS-over-HTTPS (DoH) make detection more difficult.

The general approach for detecting DNS tunneling would be to look for suspicious behavior in patterns of network traffic. Such patterns include:

* An unusual number of DNS requests to a particular server and the corresponding responses. Especially suspicious is traffic that is directly between a client and a server outside of the organisational network: most of the time tunneling is indeed point to point;  
* Regular and consistent packet sizes in queries and responses;  
* Client- or server-supplied data elements, such as subdomains, hostnames, record type, or EDNS data, that match Base32 or Base64 encoding schemes;


Connecting directly to the remote server and attempting to send a normal DNS request can help verify whether it is an actual DNS server or not. Incorrect responses may show that it is not being used for normal DNS operations.

### Examples

There are many open tools for setting up VPN tunnels using DNS. Network defenders should consider this a commonly accessible capability. Some examples of packages that can perform DNS tunneling are:

* [https://github.com/iagox86/dnscat2](https://github.com/iagox86/dnscat2) \- creates encrypted channels over DNS that can be used for various purposes  
* [https://code.kryo.se/iodine/](https://code.kryo.se/iodine/) \- allow tunneling generic IP packets over DNS  
* [https://github.com/iagox86/dnscat2](https://github.com/iagox86/dnscat2)  
* [https://github.com/alex-sector/dns2tcp](https://github.com/alex-sector/dns2tcp)  
* h[ttps://github.com/mosajjal/dnspot](https://github.com/mosajjal/dnspot)  
* [https://github.com/tladesignz/dnstt](https://github.com/tladesignz/dnstt) 

### Potential Resources

Some network forensics data sources to gather evidence on these patterns for detection include: 

* DNS query logs  
* IDS logs  
* Firewall logs  
* Inbound and outbound connection monitors

CISA wrote a really good guide on implementing enterprise DNS in order to detect and block DNS tunneling. [https://www.cisa.gov/sites/default/files/2024-05/Encrypted%20DNS%20Implementation%20Guidance\_508c.pdf](https://www.cisa.gov/sites/default/files/2024-05/Encrypted%20DNS%20Implementation%20Guidance_508c.pdf) 

An excellent and very thorough paper on detecting DNS tunneling is recommended here: [https://www.giac.org/paper/gcia/1116/detecting-dns-tunneling/108367](https://www.giac.org/paper/gcia/1116/detecting-dns-tunneling/108367)

A description of DNS Tunneling and how it can be abused: [DNS Tunneling: how DNS can be (ab)used by malicious actors (paloaltonetworks.com)](https://unit42.paloaltonetworks.com/dns-tunneling-how-dns-can-be-abused-by-malicious-actors/)   
