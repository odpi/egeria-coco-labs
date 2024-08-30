"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.



Egeria Coco Pharmaceutical demonstration labs.

This script configures and initiates the Egeria OMAG Servers deployed on the Development Platform.
It is automatically run whenever the Coco Lab Compose script is started.

"""

import argparse

from globals import (cocoMDSxName, devPlatformURL, cocoCohort, iotCohort, max_paging_size, dataLakePlatformURL,
                     fileSystemRoot, adminUserId)
from pyegeria import CoreServerConfig, Platform, FullServerConfig
from pyegeria import (
    print_exception_response,
)


def config_coco_development(url: str, userid: str):
    disable_ssl_warnings = True

    mdr_server = cocoMDSxName
    platform_url = devPlatformURL
    admin_user = "garygeeke"
    mdr_server_user_id = "cocoMDSxnpa"
    mdr_server_password = "cocoMDSxpassw0rd"
    metadataCollectionId = f"{mdr_server}-e915f2fa-aa3g-4396-8bde-bcd65e642b1d"
    metadataCollectionName = "Development Catalog"

    print("Configuring " + mdr_server + "...")

    try:
        o_client = CoreServerConfig(mdr_server, platform_url, admin_user)

        o_client.set_basic_server_properties("Development Server",
                                             "Coco Pharmaceuticals",
                                             platform_url,
                                             mdr_server_user_id, mdr_server_password,
                                             max_paging_size)

        event_bus_config = {
            "producer": {
                "bootstrap.servers": "host.docker.internal:7192"
            },
            "consumer": {
                "bootstrap.servers": "host.docker.internal:7192"
            }
        }

        # security_connection_body = {
        #     "class": "Connection",
        #     "connectorType": {
        #         "class": "ConnectorType",
        #         "connectorProviderClassName":
        #             "org.odpi.openmetadata.metadatasecurity.samples.CocoPharmaServerSecurityProvider"
        #     }
        # }

        security_connection_body = {
                "class": "Connection",
                "connectorType": {
                    "class": "ConnectorType",
                    "connectorProviderClassName":
                        "org.odpi.openmetadata.metadatasecurity.samples.CocoPharmaServerSecurityProvider"
                }
            }
        
        o_client.set_event_bus(event_bus_config)
        o_client.set_server_security_connection(security_connection_body)
        o_client.add_default_log_destinations()
        # o_client.set_in_mem_local_repository()
        o_client.set_xtdb_local_kv_repository()

        o_client.set_local_metadata_collection_id(metadataCollectionId)
        o_client.set_local_metadata_collection_name(metadataCollectionName)

        o_client.add_cohort_registration(cocoCohort)
        o_client.add_cohort_registration(iotCohort)

        print(f"Configuring {mdr_server}  Access Services (OMAS)....")

        access_service_options = {
            "SupportedZones": ["sdlc", "quarantine", "clinical-trials", "research", "data-lake", "trash-can"],
            "DefaultZones": ["sdlc", "quarantine"]
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
        # o_client.configure_access_service("data-manager", access_service_options)
        o_client.configure_access_service("it-infrastructure", access_service_options)
        o_client.configure_access_service("project-management", access_service_options)
        o_client.configure_access_service("software-developer", access_service_options)
        # o_client.configure_access_service("devops", access_service_options)
        o_client.configure_access_service("digital-architecture", access_service_options)
        o_client.configure_access_service("design-model", access_service_options)

        print(f"Configuring {mdr_server}")
        p_client = Platform(mdr_server, platform_url, admin_user)
        p_client.activate_server_stored_config()

        print(f"\n\n\tActivation of {mdr_server} is complete.")

    except Exception as e:
        print_exception_response(e)

    #
    # monitorDev01
    #
    daemon_server_name = "monitorDev01"
    daemon_server_platform = devPlatformURL
    daemon_server_user_id = "erinoverview"
    daemon_server_password = "erinoverviewpassw0rd"

    mdr_server = "cocoMDSx"
    platform_url = devPlatformURL

    print("Configuring " + daemon_server_name + "...")

    try:
        f_client = FullServerConfig(daemon_server_name, daemon_server_platform, admin_user)

        f_client.set_basic_server_properties("Integration daemon supporting the development team",
                                             "Coco Pharmaceuticals",
                                             daemon_server_platform,
                                             daemon_server_user_id, daemon_server_password,
                                             max_paging_size)

        security_connection_body = {
            "class": "Connection",
            "connectorType": {
                "class": "ConnectorType",
                "connectorProviderClassName":
                    "org.odpi.openmetadata.metadatasecurity.samples.CocoPharmaServerSecurityProvider"
            }
        }
        f_client.set_server_security_connection(security_connection_body)
        f_client.add_default_log_destinations()

        print(f"Initial configuration of {daemon_server_name} is complete.")

    except Exception as e:
        print_exception_response(e)


    #
    # monitorGov01
    #

    daemon_server_name = "monitorGov01"
    daemon_server_platform = dataLakePlatformURL
    daemon_server_user_id = "exchangeDL01npa"
    daemon_server_password = "exchangeDL01passw0rd"

    mdr_server = "cocoMDS1"
    mdr_platform_url = dataLakePlatformURL
    admin_user = "garygeeke"

    KafkaReceiverConnectorName = "KafkaOpenLineageEventReceiver"
    KafkaReceiverConnectorUserId = "onboardDL01npa"
    KafkaReceiverConnectorSourceName = "Apache Kafka"
    KafkaReceiverConnectorConnection = {
        "class": "VirtualConnection",
        "connectorType":
            {
                "class": "ConnectorType",
                "connectorProviderClassName": "org.odpi.openmetadata.adapters.connectors.integration.openlineage.OpenLineageEventReceiverIntegrationProvider"
            },
        "embeddedConnections":
            [
                {
                    "class": "EmbeddedConnection",
                    "embeddedConnection":
                        {
                            "class": "Connection",
                            "connectorType":
                                {
                                    "class": "ConnectorType",
                                    "connectorProviderClassName": "org.odpi.openmetadata.adapters.eventbus.topic.kafka.KafkaOpenMetadataTopicProvider",
                                },
                            "endpoint":
                                {
                                    "class": "Endpoint",
                                    "address": "openlineage.topic"
                                },
                            "configurationProperties":
                                {
                                    "producer":
                                        {
                                            "bootstrap.servers": "host.docker.internal:7192"
                                        },
                                    "local.server.id": "f234e808-2d0c-4d88-83df-275eee20c1b7",
                                    "consumer":
                                        {
                                            "bootstrap.servers": "host.docker.internal:7192"
                                        }
                                }
                        }
                }
            ]
    }

    GovernanceActionConnectorName = "GovernanceActionOpenLineageCreator"
    GovernanceActionConnectorUserId = "onboardDL01npa"
    GovernanceActionConnectorSourceName = "Egeria"
    GovernanceActionConnectorConnection = {
        "class": "Connection",
        "connectorType":
            {
                "class": "ConnectorType",
                "connectorProviderClassName": "org.odpi.openmetadata.adapters.connectors.integration.openlineage.GovernanceActionOpenLineageIntegrationProvider"
            },
    }

    APILoggerConnectorName = "APIBasedOpenLineageLogStore"
    APILoggerConnectorUserId = "onboardDL01npa"
    APILoggerConnectorSourceName = "Egeria"
    APILoggerConnectorConnection = {
        "class": "Connection",
        "connectorType":
            {
                "class": "ConnectorType",
                "connectorProviderClassName": "org.odpi.openmetadata.adapters.connectors.integration.openlineage.APIBasedOpenLineageLogStoreProvider"
            },
        "endpoint":
            {
                "class": "Endpoint",
                "address": "http://localhost:5000/api/v1/lineage"
            }
    }

    FileLoggerConnectorName = "FileBasedOpenLineageLogStore"
    FileLoggerConnectorUserId = "onboardDL01npa"
    FileLoggerConnectorSourceName = "Egeria"
    FileLoggerConnectorConnection = {
        "class": "Connection",
        "connectorType":
            {
                "class": "ConnectorType",
                "connectorProviderClassName": "org.odpi.openmetadata.adapters.connectors.integration.openlineage.FileBasedOpenLineageLogStoreProvider"
            },
        "endpoint":
            {
                "class": "Endpoint",
                "address": fileSystemRoot + '/openlineage.log'
            }
    }

    CataloguerConnectorName = "OpenLineageCataloguer"
    CataloguerConnectorUserId = "onboardDL01npa"
    CataloguerConnectorSourceName = "OpenLineageSources"
    CataloguerConnectorConnection = {
        "class": "Connection",
        "connectorType":
            {
                "class": "ConnectorType",
                "connectorProviderClassName": "org.odpi.openmetadata.adapters.connectors.integration.openlineage.OpenLineageCataloguerIntegrationProvider"
            }
    }

    print("Configuring " + daemon_server_name )

    connectorConfigs = [
        {
            "class": "IntegrationConnectorConfig",
            "connectorName": KafkaReceiverConnectorName,
            "connectorUserId": KafkaReceiverConnectorUserId,
            "connection": KafkaReceiverConnectorConnection,
            "metadataSourceQualifiedName": KafkaReceiverConnectorSourceName,
            "refreshTimeInterval": 10,
            "usesBlockingCalls": "false"
        },
        {
            "class": "IntegrationConnectorConfig",
            "connectorName": GovernanceActionConnectorName,
            "connectorUserId": GovernanceActionConnectorUserId,
            "connection": GovernanceActionConnectorConnection,
            "metadataSourceQualifiedName": GovernanceActionConnectorSourceName,
            "refreshTimeInterval": 10,
            "usesBlockingCalls": "false"
        },
        {
            "class": "IntegrationConnectorConfig",
            "connectorName": APILoggerConnectorName,
            "connectorUserId": APILoggerConnectorUserId,
            "connection": APILoggerConnectorConnection,
            "metadataSourceQualifiedName": APILoggerConnectorSourceName,
            "refreshTimeInterval": 10,
            "usesBlockingCalls": "false"
        },
        {
            "class": "IntegrationConnectorConfig",
            "connectorName": FileLoggerConnectorName,
            "connectorUserId": FileLoggerConnectorUserId,
            "connection": FileLoggerConnectorConnection,
            "metadataSourceQualifiedName": FileLoggerConnectorSourceName,
            "refreshTimeInterval": 10,
            "usesBlockingCalls": "false"
        },
        {
            "class": "IntegrationConnectorConfig",
            "connectorName": CataloguerConnectorName,
            "connectorUserId": CataloguerConnectorUserId,
            "connection": CataloguerConnectorConnection,
            "metadataSourceQualifiedName": CataloguerConnectorSourceName,
            "refreshTimeInterval": 10,
            "usesBlockingCalls": "false"
        }]

    print("\nDone.")

    try:
        f_client = FullServerConfig(daemon_server_name, daemon_server_platform, admin_user)

        f_client.set_basic_server_properties("An Engine Host to run governance actions for Coco Pharmaceuticals",
                                             "Coco Pharmaceuticals",
                                             daemon_server_platform,
                                             daemon_server_user_id, daemon_server_password,
                                             max_paging_size)

        security_connection_body = {
            "class": "Connection",
            "connectorType": {
                "class": "ConnectorType",
                "connectorProviderClassName":
                    "org.odpi.openmetadata.metadatasecurity.samples.CocoPharmaServerSecurityProvider"
            }
        }
        f_client.set_server_security_connection(security_connection_body)
        f_client.add_default_log_destinations()

        f_client.config_integration_service(mdr_server, mdr_platform_url,
                                            "lineage-integrator", {}, connectorConfigs)

        print(f"Activating {daemon_server_name}")
        p_client = Platform(daemon_server_name, daemon_server_platform, admin_user)
        p_client.activate_server_stored_config()
        print(f"Activation of {daemon_server_name} complete")
    except Exception as e:
        print_exception_response(e)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--url", help="URL Platform to connect to")
    parser.add_argument("--userid", help="User Id")
    args = parser.parse_args()

    url = args.url if args.url is not None else devPlatformURL
    userid = args.userid if args.userid is not None else adminUserId

    config_coco_development(url, userid)

if __name__ == "__main__":
    main()