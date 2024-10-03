from unittest import mock
from uuid import uuid4

from boto3 import client
from moto import mock_aws

from tests.providers.aws.utils import (
    AWS_ACCOUNT_NUMBER,
    AWS_REGION_EU_WEST_1,
    set_mocked_aws_provider,
)

CLUSTER_ID = str(uuid4())
CLUSTER_ARN = (
    f"arn:aws:redshift:{AWS_REGION_EU_WEST_1}:{AWS_ACCOUNT_NUMBER}:cluster:{CLUSTER_ID}"
)


class Test_redshift_cluster_non_default_database_name:
    def test_no_clusters(self):
        from prowler.providers.aws.services.redshift.redshift_service import Redshift

        aws_provider = set_mocked_aws_provider([AWS_REGION_EU_WEST_1])

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=aws_provider,
        ):
            with mock.patch(
                "prowler.providers.aws.services.redshift.redshift_cluster_non_default_database_name.redshift_cluster_non_default_database_name.redshift_client",
                new=Redshift(aws_provider),
            ):
                from prowler.providers.aws.services.redshift.redshift_cluster_non_default_database_name.redshift_cluster_non_default_database_name import (
                    redshift_cluster_non_default_database_name,
                )

                check = redshift_cluster_non_default_database_name()
                result = check.execute()

                assert len(result) == 0

    @mock_aws
    def test_cluster_default_database_name(self):
        redshift_client = client("redshift", region_name=AWS_REGION_EU_WEST_1)
        redshift_client.create_cluster(
            DBName="dev",
            ClusterIdentifier=CLUSTER_ID,
            ClusterType="single-node",
            NodeType="ds2.xlarge",
            MasterUsername="awsuser",
            MasterUserPassword="password",
            PubliclyAccessible=True,
            Tags=[
                {"Key": "test", "Value": "test"},
            ],
            Port=9439,
            Encrypted=False,
        )
        from prowler.providers.aws.services.redshift.redshift_service import Redshift

        aws_provider = set_mocked_aws_provider([AWS_REGION_EU_WEST_1])

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=aws_provider,
        ):
            with mock.patch(
                "prowler.providers.aws.services.redshift.redshift_cluster_non_default_database_name.redshift_cluster_non_default_database_name.redshift_client",
                new=Redshift(aws_provider),
            ):
                from prowler.providers.aws.services.redshift.redshift_cluster_non_default_database_name.redshift_cluster_non_default_database_name import (
                    redshift_cluster_non_default_database_name,
                )

                check = redshift_cluster_non_default_database_name()
                result = check.execute()

                assert len(result) == 1
                assert result[0].status == "FAIL"
                assert result[0].status_extended == (
                    f"Redshift Cluster {CLUSTER_ID} has the default database name: dev."
                )
                assert result[0].resource_id == CLUSTER_ID
                assert result[0].resource_arn == CLUSTER_ARN
                assert result[0].region == AWS_REGION_EU_WEST_1
                assert result[0].resource_tags == [{"Key": "test", "Value": "test"}]

    @mock_aws
    def test_cluster_non_default_database_name(self):
        redshift_client = client("redshift", region_name=AWS_REGION_EU_WEST_1)
        redshift_client.create_cluster(
            DBName="test",
            ClusterIdentifier=CLUSTER_ID,
            ClusterType="single-node",
            NodeType="ds2.xlarge",
            MasterUsername="user",
            MasterUserPassword="password",
            PubliclyAccessible=True,
            Tags=[
                {"Key": "test", "Value": "test"},
            ],
            Port=9439,
            Encrypted=True,
        )
        from prowler.providers.aws.services.redshift.redshift_service import Redshift

        aws_provider = set_mocked_aws_provider([AWS_REGION_EU_WEST_1])

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=aws_provider,
        ):
            with mock.patch(
                "prowler.providers.aws.services.redshift.redshift_cluster_non_default_database_name.redshift_cluster_non_default_database_name.redshift_client",
                new=Redshift(aws_provider),
            ):
                from prowler.providers.aws.services.redshift.redshift_cluster_non_default_database_name.redshift_cluster_non_default_database_name import (
                    redshift_cluster_non_default_database_name,
                )

                check = redshift_cluster_non_default_database_name()
                result = check.execute()

                assert len(result) == 1
                assert result[0].status == "PASS"
                assert result[0].status_extended == (
                    f"Redshift Cluster {CLUSTER_ID} does not have the default database name."
                )
                assert result[0].resource_id == CLUSTER_ID
                assert result[0].resource_arn == CLUSTER_ARN
                assert result[0].region == AWS_REGION_EU_WEST_1
                assert result[0].resource_tags == [{"Key": "test", "Value": "test"}]