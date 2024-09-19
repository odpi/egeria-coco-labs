<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the ODPi Egeria project. -->

# Open Metadata Labs - Using Docker Compose

The open metadata labs provide an interactive environment that allows you to
experiment with different capabilities of Egeria.  More information about the labs can be found at:
[Overview of the Labs](https://egeria-project.org/education/open-metadata-labs/overview/).
The labs are written using Python Jupyter notebooks that
run in a Jupyter Server. The interactive exercises in the notebooks call python functions
that communicate with Egeria. An Apache Kafka server is used by Egeria for communications.

One way to easily deploy a running
Open Metadata Labs environment is by using the Docker Compose script contained in this directory.

A docker compose script, coco-lab-setup.yaml uses docker compose to deploy, configure and run a complete working 
environment that includes:

* Three Egeria OMAG Server Platforms (Core, Datalake, and Development)
* Kafka
* Jupyter Server that is used to run the lab exercises
* Unity Catalog Open Source Server


# Getting Started

To get started, you need a computer with Docker installed and configured. Our experience is with running Docker on Mac and 
Linux machines, Windows machines should also work (reach out if you run into issues). Docker can be installed from 
[Docker](https://docker.com). Compatible alternatives to Docker Compose exist but have not yet been validated by us.

The steps to get started are:
1) If not already installed in your environment, install and start Docker and Docker Compose. If you are running on a local machine, then it is often simplest to install `Docker Desktop`.
2) Download the github repo. You can download and unpack a zip file of the repo or clone the repo if you have **git** set up:
    a) download the zipfile by navigating to `https://github.com/odpi/egeria-coco-labs` and selecting `Download ZIP` from the green Code drop down.
    b) clone the repo - `git clone https://github.com/odpi/egeria-coco-labs.git`
3) Change directory to egeria-jupyter-notebooks/coco-lab-docker-compose and start up the environment by entering `docker compose -f coco-lab-setup.yaml up --build`
This should download and install all the components, start them up and then configure the Egeria servers for the Coco labs. Once this is all done (may take a few minutes), you
can open a browser to http://localhost:7888. If it asks for a password or token, type `egeria`. You should now be in a Jupyter notebook environment. Open the `read-me-first` notebook.

Congratulations! You should be up and running!







----
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/),
Copyright Contributors to the ODPi Egeria project.
