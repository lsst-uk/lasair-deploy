# Lasair

Lasair is a broker for astronomical transients, a collaboration between
the [University of Edinburgh](https://www.ed.ac.uk/) and
[Queen's University, Belfast](https://www.qub.ac.uk/) for alerts
generated by the [Vera C. Rubin Observatory](https://www.lsst.org/). 

## Deploying Lasair

This repository contains the scripts and documentation necessary to 
deploy a new instance of Lasair.

## Preliminaries

Lasair is designed to run in an OpenStack cloud. A minimal deployment 
for development purposes is likely to require several small instances,
in addition to a more minimal bootstrap/login 
instance; a production scale deployment is likely to require 
considerably greater resources.

1. (Optional) Create a new OpenStack network for this deployment if 
required. If there are multiple Lasair deployments in the same 
OpenStack project it is probably a good idea for each one to have its
own network. 

For example:
```
$  openstack network create lasair-dev
$  openstack subnet create lasair-dev-subnet --network lasair-dev --subnet-range 10.1.1.0/24
$  openstack router create lasair-dev
$  openstack router set lasair-dev --external-gateway external
$  openstack router add subnet lasair-dev lasair-dev-subnet
```

2. Manually create an instance (in the network created above if 
applicable). This will be used to bootstrap the rest
of the deployment and as a login node. Ensure that all Lasair admins
who need to can log into this instance by adding their public
ssh keys to the authorized_keys file.

3. Install Ansible. We require version 2.10 or later.
If we are using Ubuntu 20.04 then the packaged version of Ansible is
only 2.9 so we must install using pip:
```
# apt-get update && apt-get install python3-pip && pip3 install ansible
```

4. Clone this repository:
```
$ git clone https://github.com/lsst-uk/lasair-deploy.git
```

5. Get the ```openrc.sh``` file (or possibly application credential)
for the OpenStack cloud, copy it to the login instance and source it. 

6. Set the VAULT_TOKEN environment variable, e.g.:
```
$ export VAULT_TOKEN=s.Y3BveejayDWRQhUkrJbI2T6V
```

## Configuration

Edit the ```settings.yaml``` file as required. This controls various
deployment specific parameters such as host names, numbers and flavors
of instances to create, etc.

## Login instance setup

Run the ```login.yaml``` playbook:
```
$ ansible-playbook login.yaml
```

This sets up the login instance.

## Create OpenStack resources

Run the ```openstack.yaml``` playbook:
```
$ ansible-playbook openstack.yaml
```

This creates the required instances, volumes, etc. and writes the inventory
file that will be used by subsequent playbooks.

For a clean deployment the SSH keypair to access the instances will 
be created at this point. If you have already created an SSH keypair 
(e.g. from a previous  deployment) then the local files (in ~/.ssh) 
must match the keypair in OpenStack. If this is not the case then you
will need to fix it up manually first.

It is possible to rerun this on an existing deployment in order to change
the deployment, e.g. to add extra instances, but take care as deletion
of instances/volumes etc. will not be warned!

We can validate that our hosts are all up and reachable using the test playbook:
```
$ ansible-playbook test.yaml --tags ping
```

## Set CephFS credentials

CephFS requires that an access key be looked up and stored in Vault. This is not
yet automated. The process is as follows (the deployment here is called
lasair-test and the share-user lasair-user):

Look up the key:
```
$ openstack share access list --columns access_to,access_key lasair-test
+-------------+------------------------------------------+
| access_to   | access_key                               |
+-------------+------------------------------------------+
| lasair-user | ABCDeFghIjklMnOPQrS1tUvWXyZ2Ls34LZAx7A== |
+-------------+------------------------------------------+
```

Create/update the secret in vault:
```
$ vault kv put secret/lasair/cephx 'lasair-user=ABCDeFghIjklMnOPQrS1tUvWXyZ2Ls34LZAx7A=='
Success! Data written to: secret/lasair/cephx
```

If we have multiple user/key pairs in the same secret then be sure to avoid
overwriting any others.

## Configure DNS and Security Groups

If the Lasair instance is going to be publicly accessible then 
we need to configure any required DNS records to point to
the public interfaces of the instances we just created.

We also need to add those instances to appropriate security groups to
allow access. For a production system this probably means allowing
TCP port 80 for the proxy server (or web server if they're the same)
and TCP port 9092 for kafka_pub. For a development system one might
also want to allow port 8080 to the web server from a restricted
IP range.

## Deploy Lasair

First we need to deploy the database - either a standalone MariaDB server
or a Galera cluster:
```
$ ansible-playbook database.yaml
```

We can run some checks on the database deployment:
```
$ ansible-playbook test.yaml --tags db
```

We can now go ahead and run the deployment playbook:
```
$ ansible-playbook deploy.yaml
```

The deployment playbook can be used to update Lasair.

## Test Lasair

Once Lasair is deployed/updated we can run run the full set of
post-deployment tests:
```
$ ansible-playbook test.yaml
```

## Starting MirrorMaker

Mirrormaker is responsible for pulling alerts from the upstream Kafka source.
It is not started by default. To start it, edit `deploy.yaml`. In the `kafka`
section check that the upstream source points to the correct location and 
change the variable `start_mirrormaker` to `true`. Then run:
```
$ ansible-playbook deploy.yaml --tags facts,kafka
```

To stop Mirrormaker, set `start_mirrormaker` to `false` and do the same.

## Modify a deployment

To add/remove instances:
* Edit settings.yaml and change the number/create setting of the instances as required.
* Run the command: `ansible-playbook stack.yaml`
* If you have removed instances then edit `hosts` and `/etc/hosts` to remove the entries
* If you have both removed and added instances you may need to delete `~/.ssh/known_hosts`

## Remove a deployment

To remove a deployment:
```
$ openstack stack delete <name>
```

If you are not going to recreate the deployment you can then go ahead and remove the network as well.

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

