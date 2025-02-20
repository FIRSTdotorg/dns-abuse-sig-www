<!--
----
-title: "DNS Abuse Detection: DNS As A Vector for DoS"
-...
--->
# DNS Abuse Detection: DNS as a vector for DoS

### Definition

DNS is used as a vector for Denial of Service (DoS) attacks in a number of ways.

A common situation is using DNS for reflection amplification attacks by sending queries to open recursive (resolver) servers and spoofing the IP address of the victim. The spoofed IPs would be the target of the DoS attack and can include web servers, mail servers, or any network resource.

DNS can also be used as the protocol through which a straight query flood attack can take place using a botnet or compromised servers.

In some cases, DNSSEC queries can cause increased usage of DNS server resources.

[This is part of the definition from MITRE ATT\&CK](https://attack.mitre.org/techniques/T1498/002/) for Network Denial of Service: Reflection Amplification:

"Adversaries may attempt to cause a denial of service by reflecting a high-volume of network traffic to a target. This type of Network DoS takes advantage of a third-party server intermediary that hosts and will respond to a given spoofed source IP address. This third-party server is commonly termed a reflector. An adversary accomplishes a reflection attack by sending packets to reflectors with the spoofed address of the victim. Two prominent protocols that have enabled Reflection Amplification Floods are DNS and NTP through the use of several others in the wild have been documented."

These Reflection and Amplification Floods can be directed against components of the DNS, like authoritative nameservers, rendering them unresponsive.”

### Advice

Primary means of detecting the use of DNS as a vector for DoS attacks will be network traffic analysis.

In some cases, it can appear that an organization is receiving a DDoS when they are actually being used in an amplification attack.

If outgoing bandwidth is considerably higher than incoming bandwidth, this may indicate that your DNS server is being used in an amplification attack. A stronger indication would be that the outgoing traffic is directed towards a particular target.

One indicator of an amplification attack is a large number of queries types such as ANY, TXT, or DNSKEY.

### Examples

#### DNS water torture

[https://vercara.com/resources/whats-this-nxdomain-dns-query-response-and-why-do-i-have-them](https://vercara.com/resources/whats-this-nxdomain-dns-query-response-and-why-do-i-have-them)

#### DNS amplification attack revisited

[https://www.sciencedirect.com/science/article/abs/pii/S0167404813001405](https://www.sciencedirect.com/science/article/abs/pii/S0167404813001405)

#### DNS reflection and amplification attack

[https://www.cisa.gov/news-events/alerts/2013/03/29/dns-amplification-attacks](https://www.cisa.gov/news-events/alerts/2013/03/29/dns-amplification-attacks)

#### DNSSEC DoS

[https://www.darkreading.com/cloud-security/dnssec-denial-of-service-attacks-show-fragility](https://www.darkreading.com/cloud-security/dnssec-denial-of-service-attacks-show-fragility)

### Potential Resources

* Network monitoring with netflow, SNMP, MRTG, etc. can also help here  
* DNS query logs and DNS server system logs can be used for manual checking, or fed into systems to identify DoS attacks, particularly in cases of application vulnerabilities  
* Gather information on what kind of attacks are being launched against DNS currently through community channels
