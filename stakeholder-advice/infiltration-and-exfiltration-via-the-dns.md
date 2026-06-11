<!--
---
title: "DNS Abuse Detection: Infiltration and exfiltration via the DNS"
...
-->

# DNS Abuse Detection: Infiltration and exfiltration via the DNS

### Definition

Infiltration means getting information into an organization when that is against organization policy. Exfiltration means getting information out of an organization when that is against organization policy. Therefore, detection of exfiltration generally means examining DNS queries whereas detection of infiltration generally means examining DNS response (both errors and response content).

There are a few techniques for embedding other protocols within the DNS. These are generally called “tunneling” and are handled under the [DNS Tunneling](dns-tunneling) technique. This section describes situations where data is encoded in the DNS protocol without using some other protocol. Tunneling has distinct detection and mitigation opportunities and therefore is handled separately.

Infiltration via DNS traffic, without being encoded into another protocol, is used for control (as in malware command and control).

### Advice

It’s not possible to detect an encoding for infiltration or exfiltration in general. So if someone tries to describe their product as being able to “detect all exfiltration” then this is likely untrue (formally, the proof for this would use [Rice’s Theorem](https://en.wikipedia.org/wiki/Rice%27s_theorem)).

One way of detecting infiltration and exfiltration is to look for an abnormally high number of DNS queries to an individual IP address.

Another technique is to look for repeated queries for a given resource. This may indicate the construction of data being sent over the DNS protocol.

Network managers should configure networks to detect or block outbound DNS queries from machines other than the local recursive resolver. All local DNS traffic should be configured to use the local recursive resolver. Checking network traffic for data that looks like DNS queries to servers outside your network can also highlight potential infiltration or exfiltration traffic \- e.g., any traffic on UDP port 53 to an outside target.

Tools such as the open-source [DNSExfiltrator](https://github.com/Arno0x/DNSExfiltrator) have built-in options for avoiding most of the resource consumption anomalies that might be used as prevention techniques. For example, it supports: 

* “requests throttling in order to stay more stealthy when exfiltrating data  
* reduction of the DNS request size (by default it will try to use as much bytes left available in each DNS request for efficiency)  
* reduction of the DNS label size (by default it will try to use the longest supported label size of 63 chars)”

DNS Exfiltration usually creates a large amount of queries to domains with exceptionally large FQDNs. For example, a previously-unseen domain that receives 3000 queries where the hostnames inside of the domain have more than 12 characters in their labels and seem “random”.

Because infiltration and exfiltration is a malware technique, security teams might detect it through standard endpoint protection tools. 

### Examples

* [Cobalt Strike](https://www.cobaltstrike.com/) can use various techniques that are good examples of infiltration and exfiltration via DNS

### Potential Resources

* [dns-exfil](https://github.com/rybolov/dns-exfil) can simulate DNS exfiltration to test detection mechanisms.

### Further Reading

* [MITRE \- Exfiltration Over Alternative Protocol](https://attack.mitre.org/techniques/T1048/)  
* [DNSxD: Detecting Data Exfiltration over DNS](https://pureadmin.qub.ac.uk/ws/portalfiles/portal/161785678/1570493592_CameraReady.pdf) \- from Queen’s University Belfast 

## See Also

- [DNS tunneling](dns-tunneling)
- [DNS Beacons - C2 Communication](dns-beacons-c2-communication)
- [DGA domains](dga)
- [Fast flux](fast-flux)
