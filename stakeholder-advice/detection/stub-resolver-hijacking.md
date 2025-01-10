<!--
---
title: "DNS Abuse Detection: Stub resolver hijacking"
...
-->

# DNS Abuse Detection: Stub resolver hijacking

## Definition

A stub resolver converts queries from applications on a device into DNS requests that are sent to a DNS server.

Stub resolver hijacking is where the attacker compromises the Operating System of a computer or other device with malicious code that intercepts and responds to DNS queries with rogue or malicious responses.

**NB:** For the purposes of this document, this includes modifications of the hosts file, even though this technically bypasses actual DNS lookups.

## Advice

Look for general indications of system compromise.

Frequent TLS handshake failures / HTTPS certificate errors in the browser might indicate that users of a system are being redirected to incorrect servers.

Analyze network traffic flows using NetFlow/Zeek from the endpoints outbound towards a non- safelisted resolver. Add EDR/XDR rules/syscalls for detecting anomalous resolver connection attempts, i.e. outbound DNS requests that are going to resolvers not defined in the standard system configuration.

Manually check hosts files and DNS resolver configurations for unexpected modifications.

## Examples

### DNSChanger

[https://en.wikipedia.org/wiki/DNSChanger](https://en.wikipedia.org/wiki/DNSChanger)

### Pakistani Girls Mobile Data Adware

[https://www.bleepingcomputer.com/virus-removal/remove-pakistani-girls-mobile-data](https://www.bleepingcomputer.com/virus-removal/remove-pakistani-girls-mobile-data)

### GNU libc vulnerability

[https://blog.cloudflare.com/a-tale-of-a-dns-exploit-cve-2015-7547/](https://blog.cloudflare.com/a-tale-of-a-dns-exploit-cve-2015-7547/)

### Trojan:W32/Dllpatcher.A

[https://www.f-secure.com/v-descs/trojan-w32-dllpatcher.shtml](https://www.f-secure.com/v-descs/trojan-w32-dllpatcher.shtml)

## Potential Resources

- List of locations for the hosts file under different systems  
  [https://en.wikipedia.org/wiki/Hosts\_(file)\#Location\_in\_the\_file\_system](https://en.wikipedia.org/wiki/Hosts_\(file\)#Location_in_the_file_system)  
    
- Good overview of stub resolver hijacking from Vercara  
  [https://vercara.com/resources/stub-resolver-hijacking](https://vercara.com/resources/stub-resolver-hijacking)