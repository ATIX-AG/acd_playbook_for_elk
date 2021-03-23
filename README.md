## Ansible Playbook for Foreman ACD

## Operating Systems

This demo currently supports managed hosts running CentOS 7.

## Description

This playbook aims to demonstrate the usage of Foreman ACD by installing an Elasticsearch Cluster and a connected Kibana Node.
It consists of three roles:
- firewall - a role to open the needed firewall ports on the system
- elasticsearch - a role to set up and install elasticsearch
  This role is originally taken from [github.com/elastic/ansible-elasticsearch](https://github.com/elastic/ansible-elasticsearch).
- kibana - a role to set up and install kibana
  This role is originally taken from [github.com/geerlingguy/ansible-role-kibana](https://github.com/geerlingguy/ansible-role-kibana).

The elasticsearch and kibana roles contain themselves a README to document on the complete set of their variables.

For a basic setup via ACD, the variables can be used as found in the `group_vars` directory:

`group_vars/all/main.yml`:
```yaml
---
elk_stack_version: 7.11.1  # mandatory variable to set the stack version for elastic and kibana
...
```

`group_vars/elastic_nodes/main.yml`:
```yaml
---
es_config_cluster_name: "test_cluster"
es_config_initial_master_nodes: "{{ groups['elastic_nodes'] }}"
es_config_discovery_seed_hosts: "{{ groups['elastic_nodes'] | amend_list_items(postfix=':9300') }}"
es_config_network_host: "0.0.0.0"
es_heap_size: "1g"
es_config_node_data: true
es_config_node_master: true
firewall_ports:
  - "9200/tcp"
  - "9300/tcp"
es_self_monitoring: true
...
```

`group_vars/kibana_nodes/main.yml`:
```yaml
---
kibana_elasticsearch_url: "{{ groups['elastic_nodes'] | amend_list_items(postfix=':9200',prefix='http://') }}"
firewall_ports:
  - "5601/tcp"
...
```

## Elasticsearch/Kibana Upstream Repositories

This playbook adds an upstream repository for Elasticsearch and Kibana unless you set variables to prevent it:

As stated in [github.com/elastic/ansible-elasticsearch](https://github.com/elastic/ansible-elasticsearch):
> "`es_use_repository`: Setting this to `false` will stop Ansible from using the official Elastic package from any repository configured on the system.

> `es_add_repository`: Setting this to `false` will stop Ansible from adding the official Elastic package repositories (if `es_use_repository` is `true`) if you want to use a repository already present".

`es_add_repository`: Set via `group_vars/all/main.yml` will also influence the existence of the Elasticsearch/Kibana repository on Kibana hosts. The default value inside the `kibana` role is `true`.

## Documentation

* [Application Centric Deployment Guide](https://docs.orcharhino.com/or/docs/sources/usage_guides/application_centric_deployment_guide.html) in the orcharhino documentation
* [Deploying an ELK Cluster with Application Centric Deployment](https://orcharhino.com/deploying-an-elk-cluster-with-application-centric-deployment/) blog article
