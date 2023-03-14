# Lasair Status Page

The deployment system can also be used to provision a standalone status page that
monitors whether Lasair is up and can be used to provide messages/status updates if
it goes down.

To set up the status page:

1. Create an OpenStack instance (whatever the smallest flavour is should be fine).
Allocate a floating IP.

2. Configure DNS. Configure security groups to allow incoming traffic on port
80 and 443.

3. Install Ansible.

4. Clone this repository.

5a. If you want to use a standard domain specific TLS certificate then set the
`enable_letsencypt` variable to true in `status.yaml`. This is the simplest option,
but be aware that it may cause issues if you choose to redirect other domains to 
the status page in an outage. 

5b. The alternative is to set up a wildcard TLS certificate. In this case set
`enable_letsencrypt` to false and request the certificate manually, e.g.:
```
sudo certbot certonly --manual -d *.lsst.ac.uk --agree-tos --no-bootstrap --manual-public-ip-logging-ok --preferred-challenges dns-01 -m admin@example.com
``` 
You will need to be able to create a TXT record in the DNS zone.

6. Run the status playbook to deploy an Nginx web server and status update script:
```
$ ansible-playbook status.yaml
```


---

Copyright 2022 The University of Edinburgh and Queen's University Belfast

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this code except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

