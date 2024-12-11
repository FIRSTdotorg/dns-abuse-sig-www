<!--
---
title:  FIRST DNS Abuse SIG
...
-->
# Examples of DNS Abuse Techniques


JPCERT/CC has published a list of phishing URLs that demonstrate examples of techniques including domain generation algorithms (DGAs) and malicious registrations of effective SLDs. 

We see many random meaningless TLDs that are as or more random than typo squatting. For exapmle; https://github.com/JPCERTCC/phishurl-list/blob/main/2022/202206.csv
Actors are likelier to commit DNS abuse by assigning legitimate service or company names to free-level domains/subdomains of random meaningless TLDs.

Nominet published an explanation of how dangling DNS entries can lead to vulnerability to the lame delegation and on-path DNS attack techniques. 



---


The IRS published a warning against SMS scams making use of malicious registration as well as spoofing the target organization. 

IC3 also issued a PSA on the same issue, see https://www.ic3.gov/Media/Y2022/PSA221004, which might be more helpful.

As background: 

Sender ("Caller ID"): us.reveneu.servce.4658129@anissnail[.]live  

URL #1 (in SMS/text served as redirect): hxxp://lubinaf[.]me/?irs-deducted-taxes-record=73061413

URL #2 (served as a redirect to landing page): hxxps://104.248.0.8/dika[.]php

URL #3 (landing page): hxxps://usa[.]get[.]dlsaster[.]tax/home [Note: Fraudulent domain is typosquatted on a gTLD]


---
