# DNS Abuse Detection: DNS server compromise

## Definition

DNS server compromise involves unauthorized control over, or access to, a legitimate DNS server or its records, enabling adversaries to redirect traffic, manipulate queries, force the server to return malicious IP addresses, and possibly launch several other cyberattacks.

## Advice

DNS server compromises can be detected by manually checking server configurations and verifying that they are as intended. If automated configuration is used, then comparing to the source configurations can also be useful.

Checking server logs for unusual or unauthorized access from external locations can also indicate a server compromise.

A properly deployed IDR (Intrusion Detection and Response) or IDP (Intrusion Detection and Prevention) system can also detect server compromises. There are many options available for evaluation.

Automated checking of significant DNS records, e.g. parent domain A records and NS records, can show that a compromise may have taken place.

## Example

### Global DNS Hijacking Campaign: DNS Record Manipulation at Scale

[https://cloud.google.com/blog/topics/threat-intelligence/global-dns-hijacking-campaign-dns-record-manipulation-at-scale/](https://cloud.google.com/blog/topics/threat-intelligence/global-dns-hijacking-campaign-dns-record-manipulation-at-scale/)

Details from Google Security about potentially state-sponsored hijacking via compromised DNS administration panels access through proxy servers.

## Potential Resources

* DNS configurations and configuration build sources  
* DNS resolver logs  
* Server access logs