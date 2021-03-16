## Ansible Demoplaybook for Foreman ACD

## Operating Systems

For now this demo only supports only Centos-7

## Description

This playbook aims to demonstrate the usage of Foreman ACD by installing an Elasticsearch Cluster and a connected Kibana Node. In particular in consists of three roles:
- firewall - a role to open the needed firewall ports on the system
- elasticsearch - a role to set up and install elasticsearch
  this role is originally taken from https://github.com/elastic/ansible-elasticsearch
- kibana - a role to set up and install kibana
  this role is orinally taken from https://github.com/geerlingguy/ansible-role-kibana

The elasticsearch and kibana roles contain themselves a README to document on the complete set of their variables.

For a basic setup via ACD the variables can be used as to be found in the `group_vars` directory:

group_vars/all/main.yml:
```yaml
---
elk_stack_version: 7.11.1  # mandatory variable to set the stack version for elastic and kibana
...
```


group_vars/elastic_nodes/all/main.yml:
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

group_vars/kibana/all/main.yml:
```yaml
---
kibana_elasticsearch_url: "{{ groups['elastic_nodes'] | amend_list_items(postfix=':9200',prefix='http://') }}"
firewall_ports:
  - "5601/tcp"
...
```


## Elasticsearch/Kibana Upstream Repositories

This playbook will add an upstream repository for
Elasticsearch and Kibana unless you set variables to prevent it:

As stated in <cite>[Ansible-Elasticsearch][1]</cite>.
> "`es_use_repository` Setting this to `false` will stop Ansible from using the official Elastic package from any repositoryconfigured on the system

> `es_add_repository` Setting this to `false` will stop Ansible from adding the official Elastic package repositories (if 
> es_use_repository is true) if you want to use a repo already present"


[1]: https://github.com/elastic/ansible-elasticsearch
