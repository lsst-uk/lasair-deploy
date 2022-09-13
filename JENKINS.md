# Lasair CI Environment

The deployment system can also be used to provision a continuous integration environment.
This includes a Jenkins CI server and a minimal set of Lasair components, such as
a database and Kafka broker, that some of the integration tests will interact with.

## Set up a CI server

To set up a basic CI server using a single instance:

1. Create an OpenStack instance (allow a reasonable ammount of memory and plenty of disk).
Allocate a floating IP. Allocate and attach an additional volume for Kafka.

2. Configure DNS if required. Configure security groups to allow incoming traffic on port
80 and 443.

3. Install Ansible.

4. Clone this repository.

5. There are some configuration parameters in jenkins.yaml that you may need to edit.

6. Run the ci-init playbook to do some preliminary setup:
```
$ ansible-playbook ci-init.yaml
```

7. Run the jenkins playbook to deploy a CI environment and Jenkins server:
```
$ ansible-playbook jenkins.yaml
```

## Configure Jenkin†s

1. Go to the to URL of your Jenkins server, e.g. `https://lasair-jenkins.lsst.ac.uk`

2. Enter the one time password.

3. Install the suggested plugins when prompted.

4. Create an admin user when prompted.

5. Set the URL when prompted.

## Additional plugins required

* Docker
* Docker pipeline
* GitHub Branch Source Plugin

## Setting up a job for Lasair

In the Jenkins UI:

1. Create a new job.

2. Select "pipeline".

3. Tick the "GitHub hook trigger for GITScm polling" option.

4. In the Definition dropdown, choose "Pipeline script from SCM". For the SCM dropdown, pick Git.
In the Repository URL, type (or paste) the full GitHub repo URL, e.g. `https://github.com/lsst-uk/lasair4.git`

5. Note that at the time of writing a blank in the branch specifier does not work.
To specify "any" use `*/*`.

6. In the Script Path, enter `tests/JenkinsFile`

7. Go to the GitHub project. Click on the "Settings tab", then "Webhooks", the "Add Webhook".

8. The "Payload URL" is the URL of the Jenkins server plus "github-webhook/", e.g.
`https://lasair-jenkins.lsst.ac.uk/github-webhook/`. Note the trailing slash. The "Content Type"
should be `application/json`. Other options and be left as default.

9. Go back to Jenkins and trigger a manual build.

The job should now be configured to run whenever a push is made to the 


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

