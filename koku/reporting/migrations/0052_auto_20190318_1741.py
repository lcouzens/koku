# Generated by Django 2.1.7 on 2019-03-18 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0051_auto_20190315_1458'),
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP VIEW IF EXISTS reporting_ocpcosts_summary;

            CREATE OR REPLACE VIEW reporting_ocpcosts_summary AS (
                SELECT usageli.usage_start,
                    usageli.usage_end,
                    usageli.cluster_id,
                    usageli.cluster_alias,
                    usageli.namespace,
                    usageli.pod,
                    usageli.node,
                    usageli.pod_labels,
                    COALESCE(usageli.pod_charge_cpu_core_hours, 0.0::decimal) AS pod_charge_cpu_core_hours,
                    COALESCE(usageli.pod_charge_memory_gigabyte_hours, 0.0::decimal) AS pod_charge_memory_gigabyte_hours,
                    0::decimal AS persistentvolumeclaim_charge_gb_month,
                    COALESCE(ocp_aws.infra_cost, 0) as infra_cost,
                    COALESCE(ocp_aws.project_infra_cost, 0) as project_infra_cost
                FROM reporting_ocpusagelineitem_daily_summary as usageli
                LEFT JOIN (
                    SELECT cluster_id,
                        usage_start,
                        namespace,
                        pod,
                        node,
                        sum(ocp_aws.unblended_cost / ocp_aws.shared_projects) as infra_cost,
                        sum(ocp_aws.pod_cost) as project_infra_cost
                    FROM reporting_ocpawscostlineitem_daily_summary AS ocp_aws
                    GROUP BY cluster_id,
                            usage_start,
                            namespace,
                            pod,
                            node
                ) as ocp_aws
                    ON usageli.usage_start = ocp_aws.usage_start
                        AND usageli.cluster_id = ocp_aws.cluster_id
                        AND usageli.namespace = ocp_aws.namespace
                        AND usageli.pod = ocp_aws.pod
                        AND usageli.node = ocp_aws.node

                UNION

                SELECT storageli.usage_start,
                    storageli.usage_end,
                    storageli.cluster_id,
                    storageli.cluster_alias,
                    storageli.namespace,
                    storageli.pod,
                    storageli.node,
                    storageli.volume_labels as pod_labels,
                    0::decimal AS pod_charge_cpu_core_hours,
                    0::decimal AS pod_charge_memory_gigabyte_hours,
                    COALESCE(storageli.persistentvolumeclaim_charge_gb_month, 0::decimal) AS persistentvolumeclaim_charge_gb_month,
                    COALESCE(ocp_aws.infra_cost, 0::decimal) as infra_cost,
                    COALESCE(ocp_aws.project_infra_cost, 0::decimal) as project_infra_cost
                FROM reporting_ocpstoragelineitem_daily_summary as storageli
                LEFT JOIN (
                    SELECT cluster_id,
                        usage_start,
                        namespace,
                        pod,
                        node,
                        sum(ocp_aws.unblended_cost / ocp_aws.shared_projects) as infra_cost,
                        sum(ocp_aws.pod_cost) as project_infra_cost
                    FROM reporting_ocpawscostlineitem_daily_summary AS ocp_aws
                    GROUP BY cluster_id,
                            usage_start,
                            namespace,
                            pod,
                            node
                ) as ocp_aws
                    ON storageli.usage_start = ocp_aws.usage_start
                        AND storageli.cluster_id = ocp_aws.cluster_id
                        AND storageli.namespace = ocp_aws.namespace
                        AND storageli.pod = ocp_aws.pod
                        AND storageli.node = ocp_aws.node
            )
            ;
            """
        )
    ]
