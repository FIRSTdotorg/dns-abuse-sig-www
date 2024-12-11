<!--
---
title:  FIRST DNS Abuse SIG
...
-->

# DNS Abuse SIG

## Mission

The Domain Name System (DNS) is a critical part of the Internet, including mapping domain names to IP addresses. Malicious threat actors use domain names, their corresponding technical resources, and other parts of the DNS infrastructure, including its protocols, for their malicious cyber operations. CERTs are confronted with reported DNS abuse on a continuous basis, and rely heavily on DNS analysis and infrastructure to protect their constituencies. Understanding the international customary norms applicable for detecting and mitigating DNS abuse from the perspective of the global incident response community is critical for the open Internet’s stability, security and resiliency. 


## Goals & Deliverables

1. Initially, provide a common language and a FIRST-definition of what the global incident response community understands as DNS Abuse in an operational context to protect its constituencies, as well as for purposes of global policy recommendations. 
2. Develop a classification scheme for DNS Abuse.
3. Identify common tools, techniques, and practices of malicious DNS Abuse threat actors.
4. Identify the relevant stakeholders for DNS Abuse mitigation and facilitate reasonable cooperation to mitigate DNS Abuse, including possibly recommending certain provisions be adopted in applicable registration agreements to facilitate voluntary cooperation in curbing DNS Abuse.
5. Outline possible best practices for further discussion of how to effectively mitigate DNS Abuse.
6. Outline possible best practices for each of the relevant stakeholders, 
7. Organize and/or participate in meetings or conferences on DNS Abuse, and possibly deliver relevant presentations, or coordinate their delivery as reasonably necessary in furtherance of the goals outlined above.


## DNS Abuse Techniques Matrix

Our first major publication is a matrix of DNS Abuse Techniques and Stakeholders:

 - <a href="DNS-Abuse-Techniques-Matrix_v1.1.pdf">DNS-Abuse-Techniques-Matrix_v1.1.pdf</a>

The advice currently takes the form of a matrix indicating whether a specific stakeholder can directly help with a specific technique. By “help”, we mean whether the stakeholder is in a position to detect, mitigate, or prevent the abuse technique. We have organized this information under three spreadsheets covering these incident response actions. For example, during an incident involving DNS cache poisoning, the team can go to the mitigation tab and look at the row for DNS cache poisoning, to find which stakeholders they might be able to contact to help mitigate the incident.

Thanks is given in the document, which is the result of collaboration between many people representing a wide of range roles in the DNS industry.

### Japanese Translation

Many thanks to Shoko Nakai for arranging a Japanese translation of this document, available here:

 -  <a href="DNS-Abuse-Techniques-Matrix_v1.1-ja.pdf">DNS-Abuse-Techniques-Matrix_v1.1-ja.pdf</a>

### Uses of The DNS Abuse Techniques Matrix

The Matrix has been incoporated into other work elsewhere:

 - <a href="https://github.com/MISP/misp-galaxy#first-dns-abuse-techniques-matrix">MISP Galaxy</a>
 - <a href="https://github.com/dod-cyber-crime-center/cti-stix-common-objects/blob/incident_rework/extension-definition-specifications/incident-core/Incident%20Extension%20Suite.adoc#event-type-ov">STIX Event Type Vocabulary</a>


## Meetings and Communication

We currently have a regularly scheduled weekly meeting every two weeks on Thursdays at 21:00 JST. Please note that JST doesn't follow daylight savings, so for half the world this will change twice a year. Most regular communication is done through the Slack channel, but we also have a <a href="mailto:dns-abuse-sig@first.org">mailing list</a> for members which is used for more official discussion and in cases where we need to reach the entire SIG.


## Chair

<<<<<<< HEAD
 - John Todd, Quad9
 - Jonathan Spring
 - Peter Lowe
=======
 - Jonathan Spring, CISA
 - Peter Lowe
 - Swapneel Patnekar, Shreshta IT
>>>>>>> master

## Founders

 - Carlos Alvarez
 - Trey Darley
 - Merike Kaeo
 - Michael Hausding
 - Jonathan Matkowsky

## Membership and Joining the SIG

FIRST members are automatically approved to join the SIG, and outside members are welcome to apply from the technical and academic communities in research or operational roles that work with DNS and DNS Abuse. Applications from non-FIRST members must be approved by the SIG chairs.

In general, the SIG is a technical group rather than a policy group. Policy items that impact anti-abuse efforts are obviously relevant to SIG work, however the scope of SIG work is primarily technical advice about how to navigate the existing policy landscape.

If you're interested in joining, please check out the <a href="policies">policies page</a>, which includes details on sharing information and our Code of Conduct.

<p class="ui-buttons"><a href="https://portal.first.org/g/DNS%20Abuse%20SIG" class="button color-button animated">Request to Join</a></p>
