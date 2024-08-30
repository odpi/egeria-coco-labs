#!/usr/bin/env python3
"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.



Egeria Coco Pharmaceutical demonstration labs.

This script configures and initiates the Egeria OMAG Servers deployed on the Core Platform.
It is automatically run whenever the Coco Lab Compose script is started.

"""


import json
import argparse
from datetime import datetime

from globals import (cocoMDS2Name, cocoMDS3Name, corePlatformURL, cocoCohort, devCohort, iotCohort, max_paging_size, adminUserId,
                     cocoMDS5Name, cocoMDS6Name)
from pyegeria import CoreServerConfig, Platform
from pyegeria import (
    print_exception_response,
)


def config_coco_core(url: str, userid: str):
    disable_ssl_warnings = True
    print("Configuring and activating the Datalake")
    platform_url = url
    admin_user = userid

    # event_bus_config = {
    #     "producer": {
    #         "bootstrap.servers": "{{kafkaEndpoint}}"
    #     },
    #     "consumer": {
    #         "bootstrap.servers": "{{kafkaEndpoint}}"
    #     }
    # }
    event_bus_config = {
        "producer": {
            "bootstrap.servers": "host.docker.internal:7192"
        },
        "consumer": {
            "bootstrap.servers": "host.docker.internal:7192"
        }
    }

    security_connection_body = {
        "class": "Connection",
        "connectorType": {
            "class": "ConnectorType",
            "connectorProviderClassName":
                "org.odpi.openmetadata.metadatasecurity.samples.CocoPharmaServerSecurityProvider"
        }
    }

    #
    # Configure MDS2
    #
    mdr_server = cocoMDS2Name
    mdr_server_user_id = "cocoMDS2npa"
    mdr_server_password = "cocoMDS2passw0rd"
    metadataCollectionId = f"{mdr_server}-e915f2fa-aa3g-4396-8bde-bcd65e642b1d"
    metadataCollectionName = "Governance Catalog"


    try:
        o_client = CoreServerConfig(mdr_server, platform_url, admin_user)

        o_client.set_basic_server_properties("Governance Server",
                                             "Coco Pharmaceuticals",
                                             platform_url,
                                             mdr_server_user_id, mdr_server_password,
                                             max_paging_size)

        o_client.set_event_bus(event_bus_config)
        o_client.set_server_security_connection(security_connection_body)
        o_client.add_default_log_destinations()

        # o_client.set_in_mem_local_repository()
        o_client.set_xtdb_local_kv_repository()

        o_client.set_local_metadata_collection_id(metadataCollectionId)
        o_client.set_local_metadata_collection_name(metadataCollectionName)

        o_client.add_cohort_registration(cocoCohort)
        o_client.add_cohort_registration(devCohort)
        o_client.add_cohort_registration(iotCohort)

        # o_client.configure_access_service("asset-catalog", {})
        o_client.configure_access_service("asset-consumer", {})

        o_client.configure_access_service("asset-owner", {})
        o_client.configure_access_service("community-profile",
                                          {"KarmaPointPlateau": "500"})
        # o_client.configure_access_service("glossary-view", {})
        # o_client.configure_access_service("subject-area", {})
        o_client.configure_access_service("governance-engine", {})
        o_client.configure_access_service("governance-server", {})
        o_client.configure_access_service("governance-program", {})
        # o_client.configure_access_service("data-privacy", {})
        o_client.configure_access_service("digital-architecture", {})
        o_client.configure_access_service("security-manager", {})
        o_client.configure_access_service("asset-lineage", {})
        o_client.configure_access_service("it-infrastructure", {})
        o_client.configure_access_service("project-management", {})
        print(f"Activating {mdr_server}")
        p_client = Platform(mdr_server, platform_url, admin_user)
        p_client.activate_server_stored_config()
        print(f"{mdr_server} activated")
    except Exception as e:
        print_exception_response(e)

    #
    # Configure MDS3
    #
    mdr_server = cocoMDS3Name
    mdr_server_user_id = "cocoMDS3npa"
    mdr_server_password = "cocoMD32passw0rd"
    metadataCollectionId = f"{mdr_server}-e915f2fa-aa3g-4396-8bde-bcd65e642b1d"
    metadataCollectionName = "Research Catalog"

    try:
        o_client = CoreServerConfig(mdr_server, platform_url, admin_user)

        o_client.set_basic_server_properties("Research Server",
                                             "Coco Pharmaceuticals",
                                             platform_url,
                                             mdr_server_user_id, mdr_server_password,
                                             max_paging_size)

        o_client.set_event_bus(event_bus_config)
        o_client.set_server_security_connection(security_connection_body)
        o_client.add_default_log_destinations()

        # o_client.set_in_mem_local_repository()
        o_client.set_xtdb_local_kv_repository()

        o_client.set_local_metadata_collection_id(metadataCollectionId)
        o_client.set_local_metadata_collection_name(metadataCollectionName)

        o_client.add_cohort_registration(cocoCohort)
        access_service_options = {
            "SupportedZones": ["personal-files", "clinical-trials", "research", "data-lake", "trash-can"]
            }


        o_client.configure_access_service("asset-consumer", access_service_options)

        access_service_options["DefaultZones"] = ["personal-files"]

        o_client.configure_access_service("asset-owner", access_service_options)
        o_client.configure_access_service("community-profile",
                                          {"KarmaPointPlateau": "500"})

        o_client.configure_access_service("asset-manager", access_service_options)
        o_client.configure_access_service("governance-engine", access_service_options)
        # o_client.configure_access_service("governance-server", {})
        # o_client.configure_access_service("governance-program", {})

        # o_client.configure_access_service("digital-architecture", {})
        # o_client.configure_access_service("security-manager", {})
        # o_client.configure_access_service("asset-lineage", {})
        # o_client.configure_access_service("it-infrastructure", {})
        o_client.configure_access_service("project-management", access_service_options)
        print(f"Activating {mdr_server}")
        p_client = Platform(mdr_server, platform_url, admin_user)
        p_client.activate_server_stored_config()
        print(f"{mdr_server} activated")
    except Exception as e:
        print_exception_response(e)
    #
    # Configure MDS5
    #
    disable_ssl_warnings = True

    mdr_server = cocoMDS5Name
    mdr_server_user_id = "cocoMDS5npa"
    mdr_server_password = "cocoMDS5passw0rd"
    metadataCollectionId = f"{mdr_server}-e915f2fa-aa3g-4396-8bde-bcd65e642b1d"
    metadataCollectionName = "Business Systems Catalog"

    print("Configuring " + mdr_server + "...")
    try:
        o_client = CoreServerConfig(mdr_server, platform_url, admin_user)

        o_client.set_basic_server_properties("Business Systems",
                                             "Coco Pharmaceuticals",
                                             platform_url,
                                             mdr_server_user_id, mdr_server_password,
                                             max_paging_size)

        o_client.set_event_bus(event_bus_config)
        o_client.set_server_security_connection(security_connection_body)
        o_client.add_default_log_destinations()

        # o_client.set_in_mem_local_repository()
        o_client.set_xtdb_local_kv_repository()

        o_client.set_local_metadata_collection_id(metadataCollectionId)
        o_client.set_local_metadata_collection_name(metadataCollectionName)

        o_client.add_cohort_registration(cocoCohort)

        proxy_details = ("org.odpi.openmetadata.adapters.repositoryservices.readonly.repositoryconnector." +
                         "ReadOnlyOMRSRepositoryConnectorProvider")
        o_client.set_repository_proxy_details(proxy_details)
        print(f"Activating {mdr_server}")
        p_client = Platform(mdr_server, platform_url, admin_user)
        p_client.activate_server_stored_config()
        print(f"{mdr_server} activated")
    except Exception as e:
        print_exception_response(e)

    #
    # Configure MDS6
    #
    disable_ssl_warnings = True

    mdr_server = cocoMDS6Name
    platform_url = corePlatformURL
    admin_user = "garygeeke"
    mdr_server_user_id = "cocoMDS6npa"
    mdr_server_password = "cocoMDS6passw0rd"
    metadataCollectionId = f"{mdr_server}-e915f2fa-aa3g-4396-8bde-bcd65e642b1d"
    metadataCollectionName = "Manufacturing Catalog"

    print("Configuring " + mdr_server + "...")

    try:
        o_client = CoreServerConfig(mdr_server, platform_url, admin_user)

        o_client.set_basic_server_properties("Manufacturing",
                                             "Coco Pharmaceuticals",
                                             platform_url,
                                             mdr_server_user_id, mdr_server_password,
                                             max_paging_size)

        o_client.set_event_bus(event_bus_config)

        o_client.set_server_security_connection(security_connection_body)
        o_client.add_default_log_destinations()

        # o_client.set_in_mem_local_repository()
        o_client.set_xtdb_local_kv_repository()

        o_client.set_local_metadata_collection_id(metadataCollectionId)
        o_client.set_local_metadata_collection_name(metadataCollectionName)

        o_client.add_cohort_registration(cocoCohort)
        o_client.add_cohort_registration(iotCohort)

        access_service_options = {
            "SupportedZones": ["manufacturing"],
            "DefaultZones": ["manufacturing"]
        }

        # o_client.configure_access_service("asset-catalog", access_service_options)
        o_client.configure_access_service("asset-consumer", access_service_options)
        o_client.configure_access_service("asset-owner", access_service_options)
        o_client.configure_access_service("community-profile",
                                          {"KarmaPointPlateau": "500"})
        # o_client.configure_access_service("glossary-view", {})
        o_client.configure_access_service("data-science", access_service_options)
        # o_client.configure_access_service("subject-area", {})
        o_client.configure_access_service("asset-manager", access_service_options)
        o_client.configure_access_service("governance-engine", access_service_options)
        o_client.configure_access_service("governance-server", access_service_options)
        o_client.configure_access_service("asset-owner", access_service_options)
        # o_client.configure_access_service("data-engine", access_service_options)
        o_client.configure_access_service("data-manager", access_service_options)
        o_client.configure_access_service("it-infrastructure", access_service_options)
        o_client.configure_access_service("project-management", access_service_options)

        print(f"Activating {mdr_server}")
        p_client = Platform(mdr_server, platform_url, admin_user)
        p_client.activate_server_stored_config()
        print(f"{mdr_server} activated")
    except Exception as e:
        print_exception_response(e)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--url", help="URL Platform to connect to")
    parser.add_argument("--userid", help="User Id")
    args = parser.parse_args()

    url = args.url if args.url is not None else corePlatformURL
    userid = args.userid if args.userid is not None else adminUserId

    config_coco_core(url, userid)

if __name__ == "__main__":
    main()
