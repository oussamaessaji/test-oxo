"""Unit tests for the oxo module."""

import io
import json

from docker.models import services as services_model
from flask import testing
from pytest_mock import plugin

from ostorlab.runtimes.local.models import models


def testImportScanMutation_always_shouldImportScan(
    authenticated_flask_client: testing.FlaskClient, zip_file_bytes: bytes
) -> None:
    """Test importScan mutation."""
    with models.Database() as session:
        nbr_scans_before_import = session.query(models.Scan).count()
        query = """
            mutation ImportScan($scanId: Int, $file: Upload!) {
                importScan(scanId: $scanId, file: $file) {
                    message
                }
            }
        """
        file_name = "imported_zip_file.zip"
        data = {
            "operations": json.dumps(
                {
                    "query": query,
                    "variables": {
                        "file": None,
                        "scanId": 20,
                    },
                }
            ),
            "map": json.dumps(
                {
                    "file": ["variables.file"],
                }
            ),
        }
        data["file"] = (io.BytesIO(zip_file_bytes), file_name)

        response = authenticated_flask_client.post(
            "/graphql", data=data, content_type="multipart/form-data"
        )

        assert response.status_code == 200, response.content
        response_json = response.get_json()
        nbr_scans_after_import = session.query(models.Scan).count()
        assert (
            response_json["data"]["importScan"]["message"]
            == "Scan imported successfully"
        )
        assert nbr_scans_after_import == nbr_scans_before_import + 1


def testQueryMultipleScans_always_shouldReturnMultipleScans(
    authenticated_flask_client: testing.FlaskClient, ios_scans: models.Scan
) -> None:
    """Test query for multiple scans."""
    with models.Database() as session:
        scans = session.query(models.Scan).filter(models.Scan.id.in_([1, 2])).all()
        assert scans is not None

    query = """
        query Scans($scanIds: [Int!]) {
            scans(scanIds: $scanIds) {
                scans {
                    id
                    title
                    asset
                    progress
                    createdTime
                }
            }
        }
    """

    response = authenticated_flask_client.post(
        "/graphql",
        json={"query": query, "variables": {"scanIds": [1, 2]}},
    )

    assert response.status_code == 200, response.get_json()
    scan1 = response.get_json()["data"]["scans"]["scans"][1]
    scan2 = response.get_json()["data"]["scans"]["scans"][0]
    assert scan1["id"] == "1"
    assert scan1["title"] == scans[0].title
    assert scan1["asset"] == scans[0].asset
    assert scan1["progress"] == scans[0].progress.name
    assert scan1["createdTime"] == scans[0].created_time.isoformat()
    assert scan2["id"] == "2"
    assert scan2["title"] == scans[1].title
    assert scan2["asset"] == scans[1].asset
    assert scan2["progress"] == scans[1].progress.name
    assert scan2["createdTime"] == scans[1].created_time.isoformat()


def testQueryMultipleScans_whenPaginationAndSortAsc_shouldReturnTheCorrectResults(
    authenticated_flask_client: testing.FlaskClient, ios_scans: models.Scan
) -> None:
    """Test query for multiple scans with pagination and sort ascending."""
    with models.Database() as session:
        scans = session.query(models.Scan).filter(models.Scan.id.in_([1, 2])).all()
        assert scans is not None

    query = """
        query Scans($scanIds: [Int!], $page: Int, $numberElements: Int, $orderBy: OxoScanOrderByEnum, $sort: SortEnum) {
            scans(scanIds: $scanIds, page: $page, numberElements: $numberElements, orderBy: $orderBy, sort: $sort) {
                scans {
                    id
                    title
                    asset
                    progress
                    createdTime
                }
            }
        }
    """

    response = authenticated_flask_client.post(
        "/graphql",
        json={
            "query": query,
            "variables": {
                "scanIds": [1, 2],
                "page": 1,
                "numberElements": 2,
                "orderBy": "ScanId",
                "sort": "Asc",
            },
        },
    )

    assert response.status_code == 200, response.get_json()
    scan1 = response.get_json()["data"]["scans"]["scans"][0]
    scan2 = response.get_json()["data"]["scans"]["scans"][1]
    assert scan1["id"] == "1"
    assert scan1["title"] == scans[0].title
    assert scan1["asset"] == scans[0].asset
    assert scan1["progress"] == scans[0].progress.name
    assert scan1["createdTime"] == scans[0].created_time.isoformat()
    assert scan2["id"] == "2"
    assert scan2["title"] == scans[1].title
    assert scan2["asset"] == scans[1].asset
    assert scan2["progress"] == scans[1].progress.name
    assert scan2["createdTime"] == scans[1].created_time.isoformat()


def testQueryMultipleScans_whenNoScanIdsSpecified_shouldReturnAllScans(
    authenticated_flask_client: testing.FlaskClient, ios_scans: models.Scan
) -> None:
    """Test query for multiple scans when no scan ids are specified."""
    with models.Database() as session:
        scans = session.query(models.Scan).all()
        assert scans is not None

    query = """
        query Scans {
            scans {
                scans {
                    id
                    title
                    asset
                    progress
                    createdTime
                }
            }
        }
    """

    response = authenticated_flask_client.post("/graphql", json={"query": query})

    assert response.status_code == 200, response.get_json()
    scan1 = response.get_json()["data"]["scans"]["scans"][1]
    scan2 = response.get_json()["data"]["scans"]["scans"][0]
    assert scan1["id"] == "1"
    assert scan1["title"] == scans[0].title
    assert scan1["asset"] == scans[0].asset
    assert scan1["progress"] == scans[0].progress.name
    assert scan1["createdTime"] == scans[0].created_time.isoformat()
    assert scan2["id"] == "2"
    assert scan2["title"] == scans[1].title
    assert scan2["asset"] == scans[1].asset
    assert scan2["progress"] == scans[1].progress.name
    assert scan2["createdTime"] == scans[1].created_time.isoformat()


def testQueryMultipleVulnerabilities_always_shouldReturnMultipleVulnerabilities(
    authenticated_flask_client: testing.FlaskClient, ios_scans: models.Scan
) -> None:
    """Test query for multiple vulnerabilities."""
    with models.Database() as session:
        vulnerabilities = (
            session.query(models.Vulnerability)
            .filter(models.Vulnerability.id.in_([1, 2]))
            .all()
        )
        assert vulnerabilities is not None
    query = """
            query Scans {
                scans {
                    scans {
                        title
                        asset
                        createdTime
                        vulnerabilities {
                            vulnerabilities {
                                technicalDetail
                                detail {
                                    title
                                }
                            }
                        }
                    }
                }
            }
    """

    response = authenticated_flask_client.post("/graphql", json={"query": query})

    assert response.status_code == 200, response.get_json()
    vulnerability = response.get_json()["data"]["scans"]["scans"][0]["vulnerabilities"][
        "vulnerabilities"
    ][0]
    assert vulnerability["technicalDetail"] == vulnerabilities[1].technical_detail
    assert vulnerability["detail"]["title"] == vulnerabilities[1].title
    vulnerability = response.get_json()["data"]["scans"]["scans"][1]["vulnerabilities"][
        "vulnerabilities"
    ][0]
    assert vulnerability["technicalDetail"] == vulnerabilities[0].technical_detail
    assert vulnerability["detail"]["title"] == vulnerabilities[0].title


def testQueryMultipleKBVulnerabilities_always_shouldReturnMultipleKBVulnerabilities(
    authenticated_flask_client: testing.FlaskClient, ios_scans: models.Scan
) -> None:
    """Test query for multiple KB vulnerabilities."""
    with models.Database() as session:
        kb_vulnerabilities = (
            session.query(models.Vulnerability)
            .filter(models.Vulnerability.id.in_([1, 2]))
            .all()
        )
        assert kb_vulnerabilities is not None
    query = """
            query Scans {
                scans {
                    scans {
                        title
                        asset
                        createdTime
                        kbVulnerabilities {
                            kb {
                                title
                                shortDescription
                                recommendation
                                references {
                                    title
                                    url
                                }
                            }
                        }
                    }
                }
            }
    """

    response = authenticated_flask_client.post("/graphql", json={"query": query})

    assert response.status_code == 200, response.get_json()
    kb_vulnerability = response.get_json()["data"]["scans"]["scans"][1][
        "kbVulnerabilities"
    ][0]["kb"]
    assert kb_vulnerability["recommendation"] == kb_vulnerabilities[0].recommendation
    assert (
        kb_vulnerability["shortDescription"] == kb_vulnerabilities[0].short_description
    )
    assert kb_vulnerability["title"] == kb_vulnerabilities[0].title
    kb_vulnerability = response.get_json()["data"]["scans"]["scans"][0][
        "kbVulnerabilities"
    ][0]["kb"]
    assert kb_vulnerability["recommendation"] == kb_vulnerabilities[1].recommendation
    assert (
        kb_vulnerability["shortDescription"] == kb_vulnerabilities[1].short_description
    )
    assert kb_vulnerability["title"] == kb_vulnerabilities[1].title
    assert (
        kb_vulnerability["references"][0]["title"]
        == "C++ Core Guidelines R.10 - Avoid malloc() and free()"
    )
    assert (
        kb_vulnerability["references"][0]["url"]
        == "https://github.com/isocpp/CppCoreGuidelines/blob/036324/CppCoreGuidelines.md#r10-avoid-malloc-and-free"
    )


def testQueryMultipleVulnerabilities_always_returnMaxRiskRating(
    authenticated_flask_client: testing.FlaskClient, android_scan: models.Scan
) -> None:
    """Test query for multiple vulnerabilities with max risk rating."""
    query = """
        query Scans {
            scans {
                scans {
                    title
                    messageStatus
                    progress
                    kbVulnerabilities {
                        highestRiskRating
                        kb {
                            title
                        }
                    }
                }
            }
        }
    """

    response = authenticated_flask_client.post("/graphql", json={"query": query})

    assert response.status_code == 200, response.get_json()
    max_risk_rating = response.get_json()["data"]["scans"]["scans"][0][
        "kbVulnerabilities"
    ][0]["highestRiskRating"]
    assert max_risk_rating == "CRITICAL"
    max_risk_rating = response.get_json()["data"]["scans"]["scans"][0][
        "kbVulnerabilities"
    ][1]["highestRiskRating"]
    assert max_risk_rating == "LOW"


def testQueryScan_whenScanExists_returnScanInfo(
    authenticated_flask_client: testing.FlaskClient, android_scan: models.Scan
) -> None:
    """Ensure the scan query returns the correct scan with all its information."""
    query = """
        query Scan ($scanId: Int!){
            scan (scanId: $scanId){
                id
                title
                asset
                createdTime
                messageStatus
                progress
                vulnerabilities {
                    vulnerabilities {
                        id
                        technicalDetail
                        riskRating
                        cvssV3Vector
                        dna
                        detail {
                            title
                            shortDescription
                            description
                            recommendation
                        }
                        cvssV3BaseScore
                    }
                }
                kbVulnerabilities {
                    highestRiskRating
                    highestCvssV3Vector
                    highestCvssV3BaseScore
                    kb {
                        title
                    }
                }
            }
        }
    """

    response = authenticated_flask_client.post(
        "/graphql", json={"query": query, "variables": {"scanId": android_scan.id}}
    )

    assert response.status_code == 200, response.get_json()
    scan_data = response.get_json()["data"]["scan"]
    assert scan_data["id"] == str(android_scan.id)
    assert scan_data["title"] == android_scan.title
    assert scan_data["progress"] == "DONE"

    vulnerabilities = scan_data["vulnerabilities"]["vulnerabilities"]
    assert len(vulnerabilities) > 0
    assert vulnerabilities[0]["riskRating"] == "LOW"
    assert vulnerabilities[0]["detail"]["title"] == "XSS"
    assert vulnerabilities[0]["detail"]["description"] == "Cross Site Scripting"


def testQueryScan_whenScanDoesNotExist_returnErrorMessage(
    authenticated_flask_client: testing.FlaskClient,
) -> None:
    """Ensure the scan query returns an error when the scan does not exist."""
    query = """
        query Scan ($scanId: Int!){
            scan (scanId: $scanId){
                id
            }
        }
    """

    response = authenticated_flask_client.post(
        "/graphql", json={"query": query, "variables": {"scanId": 42}}
    )

    assert response.status_code == 200, response.get_json()
    assert response.get_json()["errors"][0]["message"] == "Scan not found."


def testDeleteScanMutation_whenScanExist_deleteScanAndVulnz(
    authenticated_flask_client: testing.FlaskClient, android_scan: models.Scan
) -> None:
    """Ensure the delete scan mutation deletes the scan, its statuses & vulnerabilities."""
    with models.Database() as session:
        nb_scans_before_delete = session.query(models.Scan).count()
        nb_vulnz_before_delete = (
            session.query(models.Vulnerability)
            .filter_by(scan_id=android_scan.id)
            .count()
        )
        nb_status_before_delete = (
            session.query(models.ScanStatus).filter_by(scan_id=android_scan.id).count()
        )

    query = """
        mutation DeleteScan ($scanId: Int!){
            deleteScan (scanId: $scanId) {
                result
            }
        }
    """

    response = authenticated_flask_client.post(
        "/graphql", json={"query": query, "variables": {"scanId": android_scan.id}}
    )

    assert response.status_code == 200, response.get_json()
    assert nb_scans_before_delete > 0
    assert nb_vulnz_before_delete > 0
    assert nb_status_before_delete > 0
    with models.Database() as session:
        assert session.query(models.Scan).count() == 0
        assert (
            session.query(models.Vulnerability)
            .filter_by(scan_id=android_scan.id)
            .count()
            == 0
        )
        assert (
            session.query(models.ScanStatus).filter_by(scan_id=android_scan.id).count()
            == 0
        )


def testDeleteScanMutation_whenScanDoesNotExist_returnErrorMessage(
    authenticated_flask_client: testing.FlaskClient,
) -> None:
    """Ensure the delete scan mutation returns an error message when the scan does not exist."""
    query = """
        mutation DeleteScan ($scanId: Int!){
            deleteScan (scanId: $scanId) {
                result
            }
        }
    """

    response = authenticated_flask_client.post(
        "/graphql", json={"query": query, "variables": {"scanId": 42}}
    )

    assert response.status_code == 200, response.get_json()
    assert response.get_json()["errors"][0]["message"] == "Scan not found."


def testScansQuery_withPagination_shouldReturnPageInfo(
    authenticated_flask_client: testing.FlaskClient,
    ios_scans: models.Scan,
    web_scan: models.Scan,
) -> None:
    """Test the scan query with pagination, should return the correct pageInfo."""

    with models.Database() as session:
        scans = session.query(models.Scan).all()
        assert scans is not None

    query = """query Scans($scanIds: [Int!], $page: Int, $numberElements: Int) {
  scans(scanIds: $scanIds, page: $page, numberElements: $numberElements) {
    pageInfo{
      count
      numPages
      hasNext
      hasPrevious
    }
    scans {
      id
    }
  }
}
"""

    response = authenticated_flask_client.post(
        "/graphql", json={"query": query, "variables": {"page": 1, "numberElements": 2}}
    )

    assert response.status_code == 200, response.get_json()
    assert response.get_json()["data"]["scans"]["pageInfo"] == {
        "count": 3,
        "hasNext": True,
        "hasPrevious": False,
        "numPages": 2,
    }


def testVulnerabilitiesQuery_withPagination_shouldReturnPageInfo(
    authenticated_flask_client: testing.FlaskClient,
    android_scan: models.Scan,
) -> None:
    """Test the vulnerabilities query with pagination, should return the correct pageInfo."""

    with models.Database() as session:
        vulnerabilities = session.query(models.Vulnerability).all()
        assert vulnerabilities is not None

    query = """query Scans($scanIds: [Int!], $scanPage: Int, $scanElements: Int, $vulnPage: Int, $vulnElements: Int) {
        scans(scanIds: $scanIds, page: $scanPage, numberElements: $scanElements) {
            pageInfo {
                count
                numPages
                hasNext
                hasPrevious
            }
            scans {
                id
                title
                vulnerabilities(page: $vulnPage, numberElements: $vulnElements) {
                    pageInfo {
                        count
                        numPages
                        hasNext
                        hasPrevious
                    }
                    vulnerabilities {
                        id
                    }
                }
            }
        }
    }
    """

    response = authenticated_flask_client.post(
        "/graphql",
        json={
            "query": query,
            "variables": {
                "scanPage": 1,
                "scanElements": 1,
                "vulnPage": 2,
                "vulnElements": 1,
            },
        },
    )

    assert response.status_code == 200, response.get_json()
    assert response.get_json()["data"]["scans"]["scans"][0]["vulnerabilities"][
        "pageInfo"
    ] == {
        "count": 4,
        "hasNext": True,
        "hasPrevious": True,
        "numPages": 4,
    }


def testQueryAllAgentGroups_always_shouldReturnAllAgentGroups(
    authenticated_flask_client: testing.FlaskClient, agent_groups: models.AgentGroup
) -> None:
    """Test query for multiple agent groups."""
    with models.Database() as session:
        agent_groups = (
            session.query(models.AgentGroup)
            .filter(models.AgentGroup.id.in_([1, 2]))
            .all()
        )
        assert agent_groups is not None

    query = """
            query AgentGroups ($orderBy: AgentGroupOrderByEnum, $sort: SortEnum){
                agentGroups (orderBy: $orderBy, sort: $sort) {
                    agentGroups {
                        id
                        name
                        description
                        createdTime
                        key
                        agents {
                            agents {
                                id
                                key
                                args {
                                    args {
                                        id
                                        name
                                        type
                                        description
                                        value
                                    }
                                }
                            }
                        }
                    }
                }
            }
    """

    response = authenticated_flask_client.post(
        "/graphql",
        json={"query": query, "variables": {"orderBy": "AgentGroupId", "sort": "Asc"}},
    )

    assert response.status_code == 200, response.get_json()
    agent_groups_data = response.get_json()["data"]["agentGroups"]["agentGroups"]
    assert len(agent_groups_data) == 2
    agent_group1 = agent_groups_data[0]
    agent_group2 = agent_groups_data[1]
    assert agent_group1["name"] == agent_groups[0].name
    assert agent_group1["description"] == agent_groups[0].description
    assert agent_group1["key"] == f"agentgroup/{agent_groups[0].name}"
    assert agent_group1["createdTime"] == agent_groups[0].created_time.isoformat()
    assert agent_group2["name"] == agent_groups[1].name
    assert agent_group2["description"] == agent_groups[1].description
    assert agent_group2["key"] == f"agentgroup/{agent_groups[1].name}"
    assert agent_group2["createdTime"] == agent_groups[1].created_time.isoformat()
    agent_group1_agents = agent_group1["agents"]["agents"]
    agent_group2_agents = agent_group2["agents"]["agents"]
    assert len(agent_group1_agents) == 2
    assert len(agent_group2_agents) == 1
    assert agent_group1_agents[0]["key"] == "agent/ostorlab/agent1"
    assert agent_group1_agents[1]["key"] == "agent/ostorlab/agent2"
    assert agent_group2_agents[0]["key"] == "agent/ostorlab/agent1"
    agent1_args = agent_group1_agents[0]["args"]["args"]
    agent2_args = agent_group1_agents[1]["args"]["args"]
    assert len(agent1_args) == 1
    assert len(agent2_args) == 1
    assert agent1_args[0]["name"] == "arg1"
    assert agent1_args[0]["type"] == "number"
    assert agent1_args[0]["value"] == "42"
    assert agent2_args[0]["name"] == "arg2"
    assert agent2_args[0]["type"] == "string"
    assert agent2_args[0]["value"] == "hello"


def testQuerySingleAgentGroup_always_shouldReturnSingleAgentGroup(
    authenticated_flask_client: testing.FlaskClient, agent_groups: models.AgentGroup
) -> None:
    """Test query for a single agent group."""
    with models.Database() as session:
        agent_group = session.query(models.AgentGroup).filter_by(id=1).first()
        assert agent_group is not None

    query = """
            query AgentGroup ($agentGroupIds: [Int!]){
                agentGroups (agentGroupIds: $agentGroupIds) {
                    agentGroups {
                        id
                        name
                        description
                        createdTime
                        key
                        agents {
                            agents {
                                id
                                key
                                args {
                                    args {
                                        id
                                        name
                                        type
                                        description
                                        value
                                    }
                                }
                            }
                        }
                    }
                }
            }
    """

    response = authenticated_flask_client.post(
        "/graphql", json={"query": query, "variables": {"agentGroupIds": [1]}}
    )

    assert response.status_code == 200, response.get_json()
    agent_groups_data = response.get_json()["data"]["agentGroups"]["agentGroups"]
    assert len(agent_groups_data) == 1
    agent_group_data = agent_groups_data[0]
    assert agent_group_data["name"] == agent_group.name
    assert agent_group_data["description"] == agent_group.description
    assert agent_group_data["key"] == f"agentgroup/{agent_group.name}"
    assert agent_group_data["createdTime"] == agent_group.created_time.isoformat()
    agent_group_agents = agent_group_data["agents"]["agents"]
    assert len(agent_group_agents) == 2
    assert agent_group_agents[0]["key"] == "agent/ostorlab/agent1"
    assert agent_group_agents[1]["key"] == "agent/ostorlab/agent2"
    agent1_args = agent_group_agents[0]["args"]["args"]
    agent2_args = agent_group_agents[1]["args"]["args"]
    assert len(agent1_args) == 1
    assert len(agent2_args) == 1
    assert agent1_args[0]["name"] == "arg1"
    assert agent1_args[0]["type"] == "number"
    assert agent1_args[0]["value"] == "42"
    assert agent2_args[0]["name"] == "arg2"
    assert agent2_args[0]["type"] == "string"
    assert agent2_args[0]["value"] == "hello"


def testQueryAgentGroupsWithPagination_always_returnPageInfo(
    authenticated_flask_client: testing.FlaskClient, agent_groups: models.AgentGroup
) -> None:
    """Test query for agent groups with pagination."""
    with models.Database() as session:
        agent_groups = session.query(models.AgentGroup).all()
        assert agent_groups is not None

    query = """
            query AgentGroups ($page: Int, $numberElements: Int, $orderBy: AgentGroupOrderByEnum, $sort: SortEnum){
                agentGroups (page: $page, numberElements: $numberElements, orderBy: $orderBy, sort: $sort) {
                    agentGroups {
                        id
                        name
                        description
                        createdTime
                        key
                        agents {
                            agents {
                                id
                                key
                                args {
                                    args {
                                        id
                                        name
                                        type
                                        description
                                        value
                                    }
                                }
                            }
                        }
                    }
                    pageInfo {
                        count
                        numPages
                        hasPrevious
                        hasNext
                    }
                }
            }
    """

    response = authenticated_flask_client.post(
        "/graphql",
        json={
            "query": query,
            "variables": {
                "page": 2,
                "numberElements": 1,
                "orderBy": "AgentGroupId",
                "sort": "Asc",
            },
        },
    )

    assert response.status_code == 200, response.get_json()
    response_data = response.get_json()["data"]["agentGroups"]

    agent_groups_data = response_data["agentGroups"]
    page_info = response_data["pageInfo"]

    assert len(agent_groups_data) == 1

    agent_group = agent_groups_data[0]
    assert agent_group["name"] == agent_groups[1].name
    assert agent_group["description"] == agent_groups[1].description
    assert agent_group["key"] == f"agentgroup/{agent_groups[1].name}"
    assert agent_group["createdTime"] == agent_groups[1].created_time.isoformat()
    assert page_info["count"] == 2
    assert page_info["numPages"] == 2
    assert page_info["hasPrevious"] is True
    assert page_info["hasNext"] is False


def testQueryMultipleScans_whenApiKeyIsInvalid_returnUnauthorized(
    unauthenticated_flask_client: testing.FlaskClient, ios_scans: models.Scan
) -> None:
    """Test query for multiple scans when the API key is invalid."""
    query = """
        query Scans {
            scans {
                scans {
                    id
                    title
                    asset
                    progress
                    createdTime
                }
            }
        }
    """

    response = unauthenticated_flask_client.post(
        "/graphql", json={"query": query}, headers={"X-API-KEY": "invalid"}
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Unauthorized"


def testStopScanMutation_whenScanIsRunning_shouldStopScan(
    authenticated_flask_client: testing.FlaskClient,
    in_progress_web_scan: models.Scan,
    mocker: plugin.MockerFixture,
) -> None:
    """Test stopScan mutation when scan is running should stop scan."""

    mocker.patch(
        "docker.DockerClient.services", return_value=services_model.ServiceCollection()
    )
    mocker.patch("docker.DockerClient.services.list", return_value=[])
    mocker.patch("docker.models.networks.NetworkCollection.list", return_value=[])
    mocker.patch("docker.models.configs.ConfigCollection.list", return_value=[])

    with models.Database() as session:
        nbr_scans_before = session.query(models.Scan).count()
        scan = session.query(models.Scan).get(in_progress_web_scan.id)
        scan_progress = scan.progress
        query = """
            mutation stopScan($scanId: Int!){
  stopScan(scanId: $scanId){
    scan{
      id
    }
  }
}
        """
        response = authenticated_flask_client.post(
            "/graphql", json={"query": query, "variables": {"scanId": str(scan.id)}}
        )

        assert response.status_code == 200, response.get_json()
        session.refresh(scan)
        scan = session.query(models.Scan).get(in_progress_web_scan.id)
        response_json = response.get_json()
        nbr_scans_after = session.query(models.Scan).count()
        assert response_json["data"] == {
            "stopScan": {"scan": {"id": str(in_progress_web_scan.id)}}
        }
        assert scan.progress.name == "STOPPED"
        assert scan.progress != scan_progress
        assert nbr_scans_after == nbr_scans_before


def testStopScanMutation_whenNoScanFound_shouldReturnError(
    authenticated_flask_client: testing.FlaskClient,
) -> None:
    """Test stopScan mutation when scan doesn't exist should return error message."""
    query = """
        mutation stopScan($scanId: Int!){
stopScan(scanId: $scanId){
scan{
  id
}
}
}
    """
    response = authenticated_flask_client.post(
        "/graphql", json={"query": query, "variables": {"scanId": "5"}}
    )

    assert response.status_code == 200, response.get_json()
    response_json = response.get_json()
    assert response_json["errors"][0]["message"] == "Scan not found."


def testRunScanMutation_whenNetworkAsset_shouldRunScan(
    authenticated_flask_client: testing.FlaskClient,
    agent_group_nmap: models.AgentGroup,
    network_asset: models.Asset,
) -> None:
    """Test importScan mutation."""
    with models.Database() as session:
        nbr_scans_before_run = session.query(models.Scan).count()
        query = """
            mutation RunScan($scan: OxoAgentScanInputType!, $install: Boolean!) {
                runScan(
                    scan: $scan
                    install: $install
                ) {
                    scan {
                        id
                        title
                    }
                }
            }
        """
        variables = {
            "scan": {
                "title": "Test Scan Network Asset",
                "assetIds": [network_asset.id],
                "agentGroupId": agent_group_nmap.id,
            },
            "install": True,
        }

        response = authenticated_flask_client.post(
            "/graphql", json={"query": query, "variables": variables}
        )

        assert response.status_code == 200, response.get_json()
        response_json = response.get_json()
        nbr_scans_after_run = session.query(models.Scan).count()
        assert nbr_scans_after_run == nbr_scans_before_run + 1
        last_scan = session.query(models.Scan).order_by(models.Scan.id.desc()).first()
        assert response_json["data"]["runScan"]["scan"]["id"] == last_scan.id
        assert (
            response_json["data"]["runScan"]["scan"]["title"]
            == "Test Scan Network Asset"
        )


def testRunScanMutation_whenUrl_shouldRunScan(
    authenticated_flask_client: testing.FlaskClient,
    agent_group_nmap: models.AgentGroup,
    url_asset: models.Url,
) -> None:
    """Test importScan mutation for Url asset."""
    with models.Database() as session:
        nbr_scans_before_run = session.query(models.Scan).count()
        query = """
            mutation RunScan($scan: OxoAgentScanInputType!, $install: Boolean!) {
                runScan(
                    scan: $scan
                    install: $install
                ) {
                    scan {
                        id
                        title
                    }
                }
            }
        """
        variables = {
            "scan": {
                "title": "Test Scan Url Asset",
                "assetIds": [url_asset.id],
                "agentGroupId": agent_group_nmap.id,
            },
            "install": True,
        }

        response = authenticated_flask_client.post(
            "/graphql", json={"query": query, "variables": variables}
        )

        assert response.status_code == 200, response.get_json()
        response_json = response.get_json()
        nbr_scans_after_run = session.query(models.Scan).count()
        assert nbr_scans_after_run == nbr_scans_before_run + 1
        last_scan = session.query(models.Scan).order_by(models.Scan.id.desc()).first()
        assert response_json["data"]["runScan"]["scan"]["id"] == last_scan.id
        assert (
            response_json["data"]["runScan"]["scan"]["title"] == "Test Scan Url Asset"
        )


def testRunScanMutation_whenAndroidFile_shouldRunScan(
    authenticated_flask_client: testing.FlaskClient,
    agent_group_trufflehog: models.AgentGroup,
    android_file_asset: models.AndroidFile,
) -> None:
    """Test importScan mutation for AndroidFile asset."""
    with models.Database() as session:
        nbr_scans_before_run = session.query(models.Scan).count()
        query = """
            mutation RunScan($scan: OxoAgentScanInputType!, $install: Boolean!) {
                runScan(
                    scan: $scan
                    install: $install
                ) {
                    scan {
                        id
                        title
                    }
                }
            }
        """
        variables = {
            "scan": {
                "title": "Test Scan Android File",
                "assetIds": [android_file_asset.id],
                "agentGroupId": agent_group_trufflehog.id,
            },
            "install": True,
        }

        response = authenticated_flask_client.post(
            "/graphql", json={"query": query, "variables": variables}
        )

        assert response.status_code == 200, response.get_json()
        response_json = response.get_json()
        nbr_scans_after_run = session.query(models.Scan).count()
        assert nbr_scans_after_run == nbr_scans_before_run + 1
        last_scan = session.query(models.Scan).order_by(models.Scan.id.desc()).first()
        assert response_json["data"]["runScan"]["scan"]["id"] == last_scan.id
        assert (
            response_json["data"]["runScan"]["scan"]["title"]
            == "Test Scan Android File"
        )


def testRunScanMutation_whenIosFile_shouldRunScan(
    authenticated_flask_client: testing.FlaskClient,
    agent_group_trufflehog: models.AgentGroup,
    ios_file_asset: models.IosFile,
) -> None:
    """Test importScan mutation for IosFile asset."""
    with models.Database() as session:
        nbr_scans_before_run = session.query(models.Scan).count()
        query = """
            mutation RunScan($scan: OxoAgentScanInputType!, $install: Boolean!) {
                runScan(
                    scan: $scan
                    install: $install
                ) {
                    scan {
                        id
                        title
                    }
                }
            }
        """
        variables = {
            "scan": {
                "title": "Test Scan Ios File",
                "assetIds": [ios_file_asset.id],
                "agentGroupId": agent_group_trufflehog.id,
            },
            "install": True,
        }

        response = authenticated_flask_client.post(
            "/graphql", json={"query": query, "variables": variables}
        )

        assert response.status_code == 200, response.get_json()
        response_json = response.get_json()
        nbr_scans_after_run = session.query(models.Scan).count()
        assert nbr_scans_after_run == nbr_scans_before_run + 1
        last_scan = session.query(models.Scan).order_by(models.Scan.id.desc()).first()
        assert response_json["data"]["runScan"]["scan"]["id"] == last_scan.id
        assert response_json["data"]["runScan"]["scan"]["title"] == "Test Scan Ios File"


def testRunScanMutation_whenAndroidStore_shouldRunScan(
    authenticated_flask_client: testing.FlaskClient,
    agent_group_inject_asset: models.AgentGroup,
    android_store: models.AndroidStore,
) -> None:
    """Test importScan mutation for AndroidStore asset."""
    with models.Database() as session:
        nbr_scans_before_run = session.query(models.Scan).count()
        query = """
            mutation RunScan($scan: OxoAgentScanInputType!, $install: Boolean!) {
                runScan(
                    scan: $scan
                    install: $install
                ) {
                    scan {
                        id
                        title
                    }
                }
            }
        """
        variables = {
            "scan": {
                "title": "Test Scan Android Store",
                "assetIds": [android_store.id],
                "agentGroupId": agent_group_inject_asset.id,
            },
            "install": True,
        }

        response = authenticated_flask_client.post(
            "/graphql", json={"query": query, "variables": variables}
        )

        assert response.status_code == 200, response.get_json()
        response_json = response.get_json()
        nbr_scans_after_run = session.query(models.Scan).count()
        assert nbr_scans_after_run == nbr_scans_before_run + 1
        last_scan = session.query(models.Scan).order_by(models.Scan.id.desc()).first()
        assert response_json["data"]["runScan"]["scan"]["id"] == last_scan.id
        assert (
            response_json["data"]["runScan"]["scan"]["title"]
            == "Test Scan Android Store"
        )


def testRunScanMutation_whenIosStore_shouldRunScan(
    authenticated_flask_client: testing.FlaskClient,
    agent_group_inject_asset: models.AgentGroup,
    ios_store: models.IosStore,
) -> None:
    """Test importScan mutation for IosStore asset."""
    with models.Database() as session:
        nbr_scans_before_run = session.query(models.Scan).count()
        query = """
            mutation RunScan($scan: OxoAgentScanInputType!, $install: Boolean!) {
                runScan(
                    scan: $scan
                    install: $install
                ) {
                    scan {
                        id
                        title
                    }
                }
            }
        """
        variables = {
            "scan": {
                "title": "Test Scan Ios Store",
                "assetIds": [ios_store.id],
                "agentGroupId": agent_group_inject_asset.id,
            },
            "install": True,
        }

        response = authenticated_flask_client.post(
            "/graphql", json={"query": query, "variables": variables}
        )

        assert response.status_code == 200, response.get_json()
        response_json = response.get_json()
        nbr_scans_after_run = session.query(models.Scan).count()
        assert nbr_scans_after_run == nbr_scans_before_run + 1
        last_scan = session.query(models.Scan).order_by(models.Scan.id.desc()).first()
        assert response_json["data"]["runScan"]["scan"]["id"] == last_scan.id
        assert (
            response_json["data"]["runScan"]["scan"]["title"] == "Test Scan Ios Store"
        )
