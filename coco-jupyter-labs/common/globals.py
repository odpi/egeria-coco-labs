#
# This file contains the common functions and definitions used in all Egeria Hands on
# Lab Notebooks. Typically these will be system-wide functions and common environment settings
#


#
# Disable certificate checking for local development use with self-signed certificate
#

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import os
os.environ['CURL_CA_BUNDLE'] = ''

#
# This is the location of the file system that is used in the lab.  It defaults to a "data" subfolder in
# the platform's home folder.  Here you will finc the runtime files of the platforms and the data files
# used in various labs.  The default value can be overridden using the "fileSystemRoot" environment variable.
#
fileSystemRoot = os.environ.get('fileSystemRoot', 'data')
#
# This is directory where the sample data from the Egeria distribution has been unpacked in.  The default value
# describes its location in an IntelliJ workspace.  The default value can be overridden using the "egeriaDistributionRoot"
# environment variable.
#
egeriaSampleDataRoot = os.environ.get('egeriaSampleDataRoot', '')
#
# Flag to enable debug, this cases extra information to be printed including rest calls request and response details
# Switching this flag to True produces a very large amount of output and is not recommended.
# A targeted use of this flag is recommended, set this before and reset this after the code you would like to produce debug
#
isDebug = False
disable_ssl_warnings = True
max_paging_size = 1200
#
# Definitions of the Coco Pharmaceuticals Environment
#

# These are the three main platforms used to run Egeria's OMAG Servers
corePlatformURL      = os.environ.get('corePlatformURL', 'https://host.docker.internal:7443')
corePlatformName     = "Core Platform"

dataLakePlatformURL  = os.environ.get('dataLakePlatformURL', 'https://host.docker.internal:7444')
dataLakePlatformName = "Data Lake Platform"

devPlatformURL       = os.environ.get('devPlatformURL', 'https://host.docker.internal:7445')
devPlatformName      = "Dev Platform"


# The OMAG Server Platforms host one to many OMAG Servers.  An OMAG Server could be
# a metadata server or a specialized governance server.  Its behavior is determined
# by a configuration document that defines which OMAG services are activated.
# All OMAG Server Platforms support the administration commands to define a server's
# configuration document.  It is also possible to create configuration documents
# through admin calls to one OMAG Server Platform and then deploy them to the
# OMAG Server Platform where they are to run.  In the Egeria hands on lab, the
# OMAG Server configuration is created on the dev platform and deployed to the
# production platforms as needed.

adminPlatformURL = devPlatformURL

# Gary Geeke is the IT Administration Lead at Coco Pharmaceuticals.
# He does all of the configuration for the OMAG Servers. Other users are introduced and make
# calls to the server as required

adminUserId   = "garygeeke"
petersUserId  = "peterprofile"
erinsUserId   = "erinoverview"
calliesUserId = "calliequartile"
faithsUserId  = "faithbroker"
harrysUserId  = "harryhopeful"

# These are the names of the metadata servers used by Coco Pharmaceuticals.  Each metadata
# server runs as an OMAG Server on one of the OMAG Server Platforms

cocoMDS1PlatformURL  = dataLakePlatformURL
cocoMDS1PlatformName = dataLakePlatformName
cocoMDS1Name         = "cocoMDS1"

cocoMDS2PlatformURL  = corePlatformURL
cocoMDS2PlatformName = corePlatformName
cocoMDS2Name         = "cocoMDS2"

cocoMDS3PlatformURL  = corePlatformURL
cocoMDS3PlatformName = corePlatformName
cocoMDS3Name         = "cocoMDS3"

cocoMDS4PlatformURL  = dataLakePlatformURL
cocoMDS4PlatformName = dataLakePlatformName
cocoMDS4Name         = "cocoMDS4"

cocoMDS5PlatformURL  = corePlatformURL
cocoMDS5PlatformName = corePlatformName
cocoMDS5Name         = "cocoMDS5"

cocoMDS6PlatformURL  = corePlatformURL
cocoMDS6PlatformName = corePlatformName
cocoMDS6Name         = "cocoMDS6"

cocoMDSxPlatformURL  = devPlatformURL
cocoMDSxPlatformName = devPlatformName
cocoMDSxName         = "cocoMDSx"

cocoOLS1PlatformName = dataLakePlatformName
cocoOLS1PlafformURL  = dataLakePlatformURL
cocoOLS1Name         = "cocoOLS1"

# The open metadata servers are linked together through the following open metadata cohorts.
# The servers linked via a cohort can exchange open metadata either through federated
# queries or metadata replication.

cocoCohort = "cocoCohort"
devCohort  = "devCohort"
iotCohort  = "iotCohort"
ctsCohort  = "ctsCohort"

# This is the view server that runs the services that support Egeria's user interface.

cocoView1PlatformURL  = dataLakePlatformURL
cocoView1PlatformName = dataLakePlatformName
cocoView1Name = "cocoView1"

# These are the names of the governance servers used in Coco Pharmaceuticals' data lake.
# Each governance server runs as an OMAG Server on the Data Lake OMAG Server Platform.
# They also connect to a metadata server to retrieve their configuration and store their
# results.

governDL01PlatformURL    = dataLakePlatformURL
governDL01PlatformName   = dataLakePlatformName
governDL01Name           = "governDL01"
governDL01ServerType     = "Engine Host"
governDL01MDS            = "cocoMDS1"

exchangeDL01PlatformURL  = dataLakePlatformURL
exchangeDL01PlatformName = dataLakePlatformName
exchangeDL01Name         = "exchangeDL01"
exchangeDL01ServerType   = "Integration Daemon"
exchangeDL01MDS          = "cocoMDS1"

monitorGov01PlatformURL  = dataLakePlatformURL
monitorGov01PlatformName = dataLakePlatformName
monitorGov01Name         = "monitorGov01"
monitorGov01ServerType   = "Integration Daemon"
monitorGov01MDS          = "cocoMDS1"

monitorDev01PlatformURL  = devPlatformURL
monitorDev01PlatformName = devPlatformName
monitorDev01Name         = "monitorDev01"
monitorDev01ServerType   = "Integration Daemon"
monitorDev01MDS          = "cocoMDSx"

