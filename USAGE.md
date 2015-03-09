
Genevieve Web-Interface Usage
====

These instructions will give a brief tour of some basic functionality of
Genevieve.  This assumes you are running the Docker image available at
[registry.hub.docker.com/u/abramconnelly/genevieve/](https://registry.hub.docker.com/u/abramconnelly/genevieve/).

---

Run Docker Image
---

Assuming Docker is installed, retreive the `abramconnelly/genevieve` Docker image:

```
$ sudo docker pull abramconnelly/genevieve
```

You will need to look for the confirmation link, so run the `genevieve` Docker image in the foreground:

```
$ sudo docker run -p 8000:8000 abramconnelly/genevieve:devel
```

---

Sign Up
----

Go to `http://locahost:8000` and sign up.

![Signup](https://github.com/abramconnelly/genevieve/blob/usage-instructions/usage/signup.png)

Once signed up you have to watch in the Docker window to see the register link, which should look something like this:

![Confirm link](https://github.com/abramconnelly/genevieve/blob/usage-instructions/usage/confirm_link.png)

Cut and paste the relevant portion of the link into your browser and activate your account.

![Confirm account](https://github.com/abramconnelly/genevieve/blob/usage-instructions/usage/confirm_activated.png)

---

Upload a Genome
----

Once your account is activated, log in.  You should be presented with the following screen:

![Sign up](https://github.com/abramconnelly/genevieve/blob/usage-instructions/usage/report_import.png)

Choose the `Import a genome` option.  Currently for the Docker image, the 23andme import option doesn't work.
Instead, choose a file to upload.  For example, here is my 23andMe data uploaded (but before submission):

![Import genome](https://github.com/abramconnelly/genevieve/blob/usage-instructions/usage/import.png)

Once submitted, a report will start to be generated.  On my system for the 23andMe data this takes a couple of minutes.
You should see activity in the Docker screen that indicates how far along the report generation process is or
if any errors occured.  While the report is being generated, you should see the following screen:

![Still processing](https://github.com/abramconnelly/genevieve/blob/usage-instructions/usage/upload_not_processed.png)

Note that I had to use [23andme2vcf](https://github.com/arrogantrobot/23andme2vcf) to convert my 23andMe data into
VCF format for this process to work.  I don't know if 23andMe allows for straight VCF export so that's something to
look into.

---

View Report
---

After the report is generated, it should be available for download.  You can go to the `genomes` page to view your
report:

![Report ready](https://github.com/abramconnelly/genevieve/blob/usage-instructions/usage/report_ready.png)

You should now be able to download a CSV report of your genome against ClinVar!

**NOTE: In it's current state, all changes are NOT PERSISTENT.  Once the Docker image has stopped ALL CHANGES WILL BE LOST.**

At this point, the docker image is only meant to test Genevieve functionality.
