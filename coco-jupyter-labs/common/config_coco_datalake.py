#!/usr/bin/env python3
"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.



Egeria Coco Pharmaceutical demonstration labs.

This script configures and initiates the Egeria OMAG Servers deployed on the Datalake Platform.
It is automatically run whenever the Coco Lab Compose script is started.

"""

import argparse

from pyegeria import CoreServerConfig, Platform, FullServerConfig
from pyegeria import (
    print_exception_response,
)

from globals import (corePlatformURL, cocoCohort, max_paging_size, cocoMDS1Name,
                     cocoMDS4Name, dataLakePlatformURL, fileSystemRoot, adminUserId)


def config_coco_datalake(url:str, userid:str):
    print("Configuring and starting the Data Lake")
    disable_ssl_warnings = True
    platform_url = url
    admin_user = userid

    #   Change the kafka configuration to reflect the distinguished kafka setting for the labs
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
    # Configure MDS1
    #

    mdr_server = cocoMDS1Name
    mdr_server_user_id = "cocoMDS1npa"
    mdr_server_password = "cocoMDS1passw0rd"
    metadataCollectionId = f"{mdr_server}-e915f2fa-aa3g-4396-8bde-bcd65e642b1d"
    metadataCollectionName = "Data Lake Operations"

    print("Configuring " + mdr_server + "...")
    try:
        o_client = CoreServerConfig(mdr_server, platform_url, admin_user)

        o_client.set_basic_server_properties(metadataCollectionName,
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
            "SupportedZones": ["quarantine", "clinical-trials", "research", "data-lake", "trash-can"]
        }

        # o_client.configure_access_service("asset-catalog", {})
        o_client.configure_access_service("asset-consumer", {})

        access_service_options["DefaultZones"] = ["quarantine"]
        access_service_options["PublishZones"] = ["data-lake"]

        # print(f"Access Service Options: {access_service_options}")

        o_client.configure_access_service("asset-manager", access_service_options)
        o_client.configure_access_service("asset-owner", access_service_options)
        o_client.configure_access_service("community-profile",
                                          {"KarmaPointPlateau": "500"})
        # o_client.configure_access_service("glossary-view", {})
        # o_client.configure_access_service("data-engine", access_service_options)
        o_client.configure_access_service("data-manager", access_service_options)
        o_client.configure_access_service("digital-architecture", access_service_options)
        o_client.configure_access_service("governance-engine", access_service_options)
        o_client.configure_access_service("governance-server", access_service_options)
        o_client.configure_access_service("asset-lineage", access_service_options)

        print(f"Activating {mdr_server}")
        p_client = Platform(mdr_server, platform_url, admin_user)
        p_client.activate_server_stored_config()
        print(mdr_server + " activated")

    except Exception as e:
        print_exception_response(e)

    #
    # Configure MDS4
    #
    mdr_server = cocoMDS4Name
    mdr_server_user_id = "cocoMDS4npa"
    mdr_server_password = "cocoMDS4passw0rd"
    metadataCollectionId = f"{mdr_server}-e915f2fa-aa3g-4396-8bde-bcd65e642b1d"
    metadataCollectionName = "Data Lake Users"
    print("Configuring " + mdr_server + "...")

    try:

        o_client = CoreServerConfig(mdr_server, platform_url, admin_user)

        o_client.set_basic_server_properties("Data Lake Users",
                                             "Coco Pharmaceuticals",
                                             platform_url,
                                             mdr_server_user_id, mdr_server_password,
                                             max_paging_size)


        o_client.set_event_bus(event_bus_config)
        o_client.set_server_security_connection(security_connection_body)
        o_client.add_default_log_destinations()

        # Note: no metadata repository or collection configuration in this server.

        o_client.add_cohort_registration(cocoCohort)

        accessServiceOptions = {
            "SupportedZones": ["data-lake"]
        }

        # o_client.configure_access_service("asset-catalog", accessServiceOptions)
        o_client.configure_access_service("asset-consumer", accessServiceOptions)
        o_client.configure_access_service("asset-owner", {})
        o_client.configure_access_service("community-profile",
                                          {"KarmaPointPlateau": "500"})
        # o_client.configure_access_service("glossary-view", {})
        o_client.configure_access_service("data-science", accessServiceOptions)

        print(f"Activating {mdr_server}")
        p_client = Platform(mdr_server, platform_url, admin_user)
        p_client.activate_server_stored_config()

        print(f"{mdr_server} activated")

    except Exception as e:
        print_exception_response(e)

    #
    # Configure exchangeDL01
    #

    daemon_server_name = "exchangeDL01"
    daemon_server_platform = platform_url
    daemon_server_user_id = "exchangeDL01npa"
    daemon_server_password = "exchangeDL01passw0rd"

    mdr_server = "cocoMDS1"
    folder_connector_name = "DropFootClinicalTrialResultsFolderMonitor"
    folder_connector_user_id = "monitorDL01npa"
    folder_connector_source_name = "DropFootClinicalTrialResults"
    folder_connector_folder = fileSystemRoot + '/data-lake/research/clinical-trials/drop-foot/weekly-measurements'
    folder_connector_connection = {
        "class": "Connection",
        "connectorType":
            {
                "class": "ConnectorType",
                "connectorProviderClassName":
                    "org.odpi.openmetadata.adapters.connectors.integration.basicfiles.DataFolderMonitorIntegrationProvider"
            },
        "endpoint":
            {
                "class": "Endpoint",
                "address": folder_connector_folder
            }
    }

    integration_group_name = "Onboarding"

    print("Configuring " + daemon_server_name)

    try:
        f_client = FullServerConfig(daemon_server_name, daemon_server_platform, admin_user)

        f_client.set_basic_server_properties("Supports exchange of metadata with third party technologies",
                                             "Coco Pharmaceuticals",
                                             daemon_server_platform,
                                             daemon_server_user_id, daemon_server_password,
                                             max_paging_size)

        f_client.set_server_security_connection(security_connection_body)
        f_client.add_default_log_destinations()

        connector_configs = [
            {
                "class": "IntegrationConnectorConfig",
                "connectorName": folder_connector_name,
                "connectorUserId": folder_connector_user_id,
                "connection": folder_connector_connection,
                "metadataSourceQualifiedName": folder_connector_source_name,
                "refreshTimeInterval": 10,
                "usesBlockingCalls": "false"
            }
        ]

        f_client.config_integration_service(mdr_server, platform_url, "files-integrator",
                                            {}, connector_configs)

        f_client.config_integration_group(mdr_server, daemon_server_platform,
                                          integration_group_name)
        print(f"Activating {daemon_server_name}")
        p_client = Platform(daemon_server_name, daemon_server_platform, adminUserId)
        p_client.activate_server_stored_config()

        print(f"{daemon_server_name} activated")

    except Exception as e:
        print_exception_response(e)

    #
    # Configure governDL01
    #
    engine_server = "governDL01"
    engine_server_platform = platform_url

    engine_server_user_id = "governDL01npa"
    engine_server_password = "governDL01passw0rd"
    mdr_server = "cocoMDS1"
    mdr_engine_server_platform = dataLakePlatformURL

    print("Configuring " + engine_server)

    try:
        o_client = CoreServerConfig(engine_server, engine_server_platform, admin_user)

        o_client.set_basic_server_properties("An Engine Host to run governance actions for Coco Pharmaceuticals",
                                             "Coco Pharmaceuticals",
                                             engine_server_platform,
                                             engine_server_user_id, engine_server_password,
                                             max_paging_size)

        o_client.set_server_security_connection(security_connection_body)

        o_client.set_engine_definitions_client_config(mdr_server, mdr_engine_server_platform)

        engine_list_body = [
            {
                "class": "EngineConfig",
                "engineQualifiedName": "AssetDiscovery",
                "engineUserId": "findItDL01npa"
            },
            {
                "class": "EngineConfig",
                "engineQualifiedName": "AssetQuality",
                "engineUserId": "findItDL01npa"
            }
        ]

        o_client.set_engine_list(engine_list_body)

        # config = o_client.get_stored_configuration()
        # print(f"The server stored configuration is {json.dumps(config, indent=4)}")
        print(f"Activating {engine_server}")
        p_client = Platform(engine_server, engine_server_platform, admin_user)
        p_client.activate_server_stored_config()
        print(f"{engine_server} activated")
    except Exception as e:
        print_exception_response(e)

    #
    # Configure cocoView1
    #

    view_server = "cocoView1"
    view_server_user_id = "cocoView1npa"
    view_server_password = "cocoView1passw0rd"
    view_server_type = "View Server"
    remote_platform_url = corePlatformURL
    remote_server_name = cocoMDS1Name

    print("Configuring " + view_server)
    try:
        f_client = FullServerConfig(view_server, platform_url, admin_user)

        f_client.set_server_user_id(view_server_user_id)
        f_client.set_server_user_password(view_server_password)
        f_client.set_organization_name("Coco Pharmaceuticals")

        f_client.set_server_description("Coco View Server")
        f_client.set_server_url_root(platform_url)
        f_client.set_event_bus(event_bus_config)
        f_client.set_server_security_connection(security_connection_body)

        f_client.add_default_log_destinations()

        f_client.config_all_view_services(remote_server_name, platform_url)
        print(f"Activating {view_server}")
        p_client = Platform(view_server, platform_url, admin_user)
        p_client.activate_server_stored_config()

        print(f"{view_server} activated")

    except Exception as e:
        print_exception_response(e)

    #
    # Configure cocoOLS1
    #

    lineageServerName = "cocoOLS1"
    lineageServerPlatform = dataLakePlatformURL

    mdrServerName = "cocoMDS1"
    mdrServerUserId = "cocoMDS1npa"
    mdrServerPassword = "secret"
    mdrServerPlatform = dataLakePlatformURL

    print("Configuring " + lineageServerName)

    requestBody = {
        "class": "OpenLineageConfig",
        "openLineageDescription": "Open Lineage Service is used for the storage and querying of lineage",
        "lineageGraphConnection": {
            "class": "Connection",
            "displayName": "Lineage Graph Connection",
            "description": "Used for storing lineage in the Open Metadata format",
            "connectorType": {
                "class": "ConnectorType",
                "connectorProviderClassName": "org.odpi.openmetadata.openconnectors.governancedaemonconnectors.lineagewarehouseconnectors.janusconnector.graph.LineageGraphConnectorProvider"
            },
            "configurationProperties": {
                "gremlin.graph": "org.janusgraph.core.JanusGraphFactory",
                "storage.backend": "berkeleyje",
                "storage.directory": "data/servers/" + lineageServerName + "/lineage-repository/berkeley",
                "index.search.backend": "lucene",
                "index.search.directory": "data/servers/" + lineageServerName + "/lineage-repository/searchindex"
            }
        },
        "accessServiceConfig": {
            "serverName": mdrServerName,
            "serverPlatformUrlRoot": mdrServerPlatform,
            "user": mdrServerUserId,
            "password": mdrServerPassword
        },
        "backgroundJobs": [
            {
                "jobName": "LineageGraphJob",
                "jobInterval": 120,
                "jobEnabled": "false"
            },
            {
                "jobName": "AssetLineageUpdateJob",
                "jobInterval": 120,
                "jobEnabled": "false",
                "jobDefaultValue": "2021-12-03T10:15:30"
            }
        ]
    }


    try:
        f_client = FullServerConfig(lineageServerName, lineageServerPlatform, admin_user)

        f_client.set_server_description("Coco View Server")
        f_client.set_server_url_root(lineageServerPlatform)
        f_client.set_event_bus(event_bus_config)
        f_client.add_default_log_destinations()

        f_client.set_lineage_warehouse_services(requestBody, lineageServerName)
        print(f"Activating {lineageServerName}")
        p_client = Platform(lineageServerName, lineageServerPlatform, admin_user)
        p_client.activate_server_stored_config()

        print(f"{lineageServerName} activated")

    except Exception as e:
        print_exception_response(e)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--url", help="URL Platform to connect to")
    parser.add_argument("--userid", help="User Id")
    args = parser.parse_args()

    url = args.url if args.url is not None else dataLakePlatformURL
    userid = args.userid if args.userid is not None else adminUserId

    config_coco_datalake(url, userid)

if __name__ == "__main__":
    main()
