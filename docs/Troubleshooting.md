# Troubleshooting

## Can't write to the ledger

Either your `did` does not have permission to write the transaction to the ledger, or the ledger nodes are in a state where they have not selected a 'primary' node.

You should get a fairly descriptive error message for the first issue.  The second issue acts more like a timeout, since there will be no response at all.

# Tools

## Restarting a Pool

`indy-cli` command:
- `ledger pool-restart action=start`
  - Running this command when connected to a `von-network` instance will not have the desireable result.  The nodes will restart but with a different configuration.

## Remove a Node from a Pool

`indy-cli` command:
- `ledger node target=<node id> alias=<nodes alias> services=`
  - Where:
    - `<node id>` is value of the `dest` attribute in the output of `read_ledger`; see below.
    - `<nodes alias>` is the name of the node.

## Validator Info

`indy-cli` command:
- `ledger get-validator-info`
  - Provides info regarding all of the pool nodes.

Example:
```
pool(localpool):wallet(endorser_wallet):did(V4S...e6f):indy> ledger get-validator-info
Validator Info:
{
        "New_Node": "Timeout",
        "Node1": {"data":{"Extractions":{"indy-node_status":[""],"journalctl_exceptions":[""],"node-control status":[""],"stops_stat":null,"upgrade_log":""},"Hardware":{"HDD_used_by_node":"76 MBs"},"Memory_profiler":["                types |   # objects |   total size","
===================== | =========== | ============","          <class 'str |       67840 |      6.87 MB","         <class 'dict |       10032 |      5.66 MB","         <class 'code |       14202 |      1.95 MB","         <class 'type |        1852 |      1.85 MB","
    <class 'set |        3243 |    942.91 KB","         <class 'list |        3975 |    633.21 KB","        <class 'tuple |        8850 |    575.45 KB","  <class 'abc.ABCMeta |         398 |    415.36 KB","      <class 'weakref |        4834 |    377.66 KB","   function
(_remove) |        1372 |    182.22 KB"],"Node_info":{"BLS_key":"4N8aUNHSgjQVgkpm8nhNEfDf6txHznoYREg9kirmJrkivgL4oSEimFF6nsQ6M41QvhM2Z33nves5vfSn9n1UwNFJBYtWVnHYMATn76vLuL3zU88KyeAYcHfsih3He6UHcXDxcaecHVz6jhCYz1P2UZn2bDVruL5wXpehgBfBaLKm3Ba","Catchup_status":{"Last_txn_3
PC_keys":{"0":{"Node2":[null,null],"Node3":[null,null],"Node4":[null,null]},"1":{},"2":{},"3":{}},"Ledger_statuses":{"0":"not_synced","1":"not_synced","2":"not_synced","3":"not_synced"},"Number_txns_in_catchup":{"0":0,"1":0,"2":0,"3":0},"Received_LedgerStatus":"","Waitin
g_consistency_proof_msgs":{"0":null,"1":null,"2":null,"3":null}},"Client_ip":"0.0.0.0","Client_port":9702,"Client_protocol":"tcp","Committed_ledger_root_hashes":{"0":"b'AtRf2HyaurKeAxcEEu5XERQNcEKLXGSPseqgr1o8kykQ'","1":"b'DJUGXN7GghUZCR4tzvcqeUaUwe5J8nxxruJd5WkX21Pb'","
2":"b'GKot5hBsd81kMupNCXHaqbhv3huEbxAFMLnpcX2hniwn'","3":"b'EaV13jjroLzkGtz1opKWcti2i6GguZ87ma9JtdXygcXH'"},"Committed_state_root_hashes":{"0":"b'2DP4HZmyJiXy7MEGAXkJRiVZuYm7K71bBARc2WWyZxDJ'","1":"b'EtfT1FdgBuktPLoYaVZvHVTaqQMMwyfBSo1xQamLDoeK'","2":"b'DfNLmH4DAHTKv63YP
FJzuRdeEtVwF5RtVnvKYHd8iLEA'"},"Count_of_replicas":2,"Freshness_status":{"0":{"Has_write_consensus":false,"Last_updated_time":"2020-01-15 14:45:38+00:00"},"1":{"Has_write_consensus":false,"Last_updated_time":"2020-01-15 14:45:38+00:00"},"2":{"Has_write_consensus":false,"
Last_updated_time":"2020-01-15 14:45:38+00:00"}},"Metrics":{"Delta":0.1,"Lambda":240,"Omega":20,"average-per-second":{"read-transactions":1.3260185769,"write-transactions":0.0},"avg backup throughput":0.0,"client avg request latencies":{"0":null,"1":null},"instances star
ted":{"0":21168750.75364713,"1":21168750.764794867},"master throughput":null,"master throughput ratio":null,"max master request latencies":0,"ordered request counts":{"0":0,"1":0},"ordered request durations":{"0":0,"1":0},"throughput":{"0":0.0,"1":0.0},"total requests":0
,"transaction-count":{"audit":156557,"config":0,"ledger":8853,"pool":6},"uptime":7395},"Mode":"discovering","Name":"Node1","Node_ip":"0.0.0.0","Node_port":9701,"Node_protocol":"tcp","Replicas_status":{"Node1:0":{"Last_ordered_3PC":[0,0],"Primary":null,"Stashed_txns":{"St
ashed_PrePrepare":0,"Stashed_checkpoints":0},"Watermarks":"0:300"},"Node1:1":{"Last_ordered_3PC":[0,0],"Primary":null,"Stashed_txns":{"Stashed_PrePrepare":0,"Stashed_checkpoints":0},"Watermarks":"0:300"}},"Requests_timeouts":{"Ordering_phase_req_timeouts":0,"Propagates_p
hase_req_timeouts":0},"Uncommitted_ledger_root_hashes":{},"Uncommitted_ledger_txns":{"0":{"Count":0},"1":{"Count":0},"2":{"Count":0},"3":{"Count":0}},"Uncommitted_state_root_hashes":{"0":"b'2DP4HZmyJiXy7MEGAXkJRiVZuYm7K71bBARc2WWyZxDJ'","1":"b'EtfT1FdgBuktPLoYaVZvHVTaqQM
MwyfBSo1xQamLDoeK'","2":"b'DfNLmH4DAHTKv63YPFJzuRdeEtVwF5RtVnvKYHd8iLEA'"},"View_change_status":{"IC_queue":{"1":{"Voters":{"Node1":{"reason":43},"Node2":{"reason":43},"Node3":{"reason":43},"Node4":{"reason":43}}}},"Last_complete_view_no":0,"Last_view_change_started_at":
"1970-01-01 00:00:00","VCDone_queue":{},"VC_in_progress":false,"View_No":0},"did":"Gw6pDLhcBcoQesN72qfotTgFa7cbuqZpkX3Xo6pLhPhv","verkey":"33nHHYKnqmtGAVfZZGoP8hpeExeH45Fo8cKmd5mcnKYk7XgWNBxkkKJ"},"Pool_info":{"Blacklisted_nodes":[],"Quorums":"{'propagate': Quorum(2), 'c
onsistency_proof': Quorum(2), 'checkpoint': Quorum(4), 'ledger_status': Quorum(4), 'observer_data': Quorum(2), 'timestamp': Quorum(2), 'ledger_status_last_3PC': Quorum(2), 'f': 1, 'reply': Quorum(2), 'bls_signatures': Quorum(5), 'commit': Quorum(5), 'n': 6, 'same_consist
ency_proof': Quorum(2), 'weak': Quorum(2), 'backup_instance_faulty': Quorum(2), 'election': Quorum(5), 'prepare': Quorum(4), 'view_change_done': Quorum(5), 'view_change': Quorum(5), 'strong': Quorum(5)}","Reachable_nodes":[["Node1",null],["Node2",null],["Node3",null],["N
ode4",null]],"Reachable_nodes_count":4,"Read_only":false,"Suspicious_nodes":"","Total_nodes_count":6,"Unreachable_nodes":[["New_Node",null],["some",null]],"Unreachable_nodes_count":2,"f_value":1},"Protocol":{},"Software":{"Indy_packages":[""],"Installed_packages":["zipp
0.5.2","yarl 1.3.0","wcwidth 0.1.7","ujson 1.33","typing 3.7.4","typing-extensions 3.7.4","timeout-decorator 0.4.0","supervisor 4.0.4","sortedcontainers 1.5.7","six 1.11.0","sha3 0.2.1","setuptools 28.8.0","semver 2.7.9","rlp 0.6.0","pyzmq 17.0.0","PyYAML 5.1.2","python3
-indy 1.10.1","python-rocksdb 0.6.9","python-dateutil 2.8.0","pytest 5.0.1","pyparsing 2.4.2","Pympler 0.5","Pygments 2.2.0","pycparser 2.19","pycares 3.0.0","py 1.8.0","psutil 5.4.3","prompt-toolkit 0.57","portalocker 0.5.7","pluggy 0.12.0","pip 9.0.3","pathlib2 2.3.4",
"packaging 19.0","orderedset 2.0","multidict 4.5.2","msgpack-python 0.4.6","more-itertools 7.2.0","meld3 1.0.2","MarkupSafe 1.1.1","libnacl 1.6.1","leveldb 0.194","lazy-object-proxy 1.4.1","jsonpickle 0.9.6","Jinja2 2.10.1","ioflo 1.5.4","intervaltree 2.1.0","indy-plenum
 1.9.0","indy-node 1.9.0","indy-anoncreds-dev 1.0.46","importlib-metadata 0.19","idna 2.8","idna-ssl 1.1.0","distro 1.3.0","Charm-Crypto 0.0.0","chardet 3.0.4","cffi 1.12.3","cchardet 2.1.4","base58 1.0.3","attrs 19.1.0","atomicwrites 1.3.0","async-timeout 3.0.1","aiosql
ite 0.10.0","aiohttp 3.5.4","aiohttp-jinja2 1.1.2","aiodns 2.0.0","indy-crypto 0.5.1"],"OS_version":"Linux-4.4.0-148-generic-x86_64-with-debian-stretch-sid","indy-node":"1.9.0","sovrin":"unknown"},"Update_time":"Wednesday, January 15, 2020 4:48:50 PM +0000","response-ver
sion":"0.0.1","timestamp":1579106930},"identifier":"V4SGRU86Z58d6TV7PBUe6f","reqId":1579106872477556200,"type":"119"},
        "Node2": {"data":{"Extractions":{"indy-node_status":[""],"journalctl_exceptions":[""],"node-control status":[""],"stops_stat":null,"upgrade_log":""},"Hardware":{"HDD_used_by_node":"76 MBs"},"Memory_profiler":["                types |   # objects |   total size","
===================== | =========== | ============","          <class 'str |       67841 |      6.87 MB","         <class 'dict |       10032 |      5.65 MB","         <class 'code |       14202 |      1.95 MB","         <class 'type |        1852 |      1.85 MB","
    <class 'set |        3243 |    942.91 KB","         <class 'list |        3975 |    633.21 KB","        <class 'tuple |        8850 |    575.45 KB","  <class 'abc.ABCMeta |         398 |    415.36 KB","      <class 'weakref |        4846 |    378.59 KB","   function
(_remove) |        1372 |    182.22 KB"],"Node_info":{"BLS_key":"37rAPpXVoxzKhz7d9gkUe52XuXryuLXoM6P6LbWDB7LSbG62Lsb33sfG7zqS8TK1MXwuCHj1FKNzVpsnafmqLG1vXN88rt38mNFs9TENzm4QHdBzsvCuoBnPH7rpYYDo9DZNJePaDvRvqJKByCabubJz3XXKbEeshzpz4Ma5QYpJqjk","Catchup_status":{"Last_txn_3
PC_keys":{"0":{"Node1":[null,null],"Node3":[null,null],"Node4":[null,null]},"1":{},"2":{},"3":{}},"Ledger_statuses":{"0":"not_synced","1":"not_synced","2":"not_synced","3":"not_synced"},"Number_txns_in_catchup":{"0":0,"1":0,"2":0,"3":0},"Received_LedgerStatus":"","Waitin
g_consistency_proof_msgs":{"0":null,"1":null,"2":null,"3":null}},"Client_ip":"0.0.0.0","Client_port":9704,"Client_protocol":"tcp","Committed_ledger_root_hashes":{"0":"b'AtRf2HyaurKeAxcEEu5XERQNcEKLXGSPseqgr1o8kykQ'","1":"b'DJUGXN7GghUZCR4tzvcqeUaUwe5J8nxxruJd5WkX21Pb'","
2":"b'GKot5hBsd81kMupNCXHaqbhv3huEbxAFMLnpcX2hniwn'","3":"b'EaV13jjroLzkGtz1opKWcti2i6GguZ87ma9JtdXygcXH'"},"Committed_state_root_hashes":{"0":"b'2DP4HZmyJiXy7MEGAXkJRiVZuYm7K71bBARc2WWyZxDJ'","1":"b'EtfT1FdgBuktPLoYaVZvHVTaqQMMwyfBSo1xQamLDoeK'","2":"b'DfNLmH4DAHTKv63YP
FJzuRdeEtVwF5RtVnvKYHd8iLEA'"},"Count_of_replicas":2,"Freshness_status":{"0":{"Has_write_consensus":false,"Last_updated_time":"2020-01-15 14:45:39+00:00"},"1":{"Has_write_consensus":false,"Last_updated_time":"2020-01-15 14:45:39+00:00"},"2":{"Has_write_consensus":false,"
Last_updated_time":"2020-01-15 14:45:39+00:00"}},"Metrics":{"Delta":0.1,"Lambda":240,"Omega":20,"average-per-second":{"read-transactions":1.3340420147,"write-transactions":0.0},"avg backup throughput":0.0,"client avg request latencies":{"0":null,"1":null},"instances star
ted":{"0":21168751.188395705,"1":21168751.197890162},"master throughput":null,"master throughput ratio":null,"max master request latencies":0,"ordered request counts":{"0":0,"1":0},"ordered request durations":{"0":0,"1":0},"throughput":{"0":0.0,"1":0.0},"total requests":
0,"transaction-count":{"audit":156557,"config":0,"ledger":8853,"pool":6},"uptime":7394},"Mode":"discovering","Name":"Node2","Node_ip":"0.0.0.0","Node_port":9703,"Node_protocol":"tcp","Replicas_status":{"Node2:0":{"Last_ordered_3PC":[0,0],"Primary":null,"Stashed_txns":{"S
tashed_PrePrepare":0,"Stashed_checkpoints":0},"Watermarks":"0:300"},"Node2:1":{"Last_ordered_3PC":[0,0],"Primary":null,"Stashed_txns":{"Stashed_PrePrepare":0,"Stashed_checkpoints":0},"Watermarks":"0:300"}},"Requests_timeouts":{"Ordering_phase_req_timeouts":0,"Propagates_
phase_req_timeouts":0},"Uncommitted_ledger_root_hashes":{},"Uncommitted_ledger_txns":{"0":{"Count":0},"1":{"Count":0},"2":{"Count":0},"3":{"Count":0}},"Uncommitted_state_root_hashes":{"0":"b'2DP4HZmyJiXy7MEGAXkJRiVZuYm7K71bBARc2WWyZxDJ'","1":"b'EtfT1FdgBuktPLoYaVZvHVTaqQ
MMwyfBSo1xQamLDoeK'","2":"b'DfNLmH4DAHTKv63YPFJzuRdeEtVwF5RtVnvKYHd8iLEA'"},"View_change_status":{"IC_queue":{"1":{"Voters":{"Node1":{"reason":43},"Node2":{"reason":43},"Node3":{"reason":43},"Node4":{"reason":43}}}},"Last_complete_view_no":0,"Last_view_change_started_at"
:"1970-01-01 00:00:00","VCDone_queue":{},"VC_in_progress":false,"View_No":0},"did":"8ECVSk179mjsjKRLWiQtssMLgp6EPhWXtaYyStWPSGAb","verkey":"72XEVLaj3htbTYyNXeJWXJCj3ffeJHTuYLtV4PdU1n72YsCzo65aBZ6"},"Pool_info":{"Blacklisted_nodes":[],"Quorums":"{'prepare': Quorum(4), 're
ply': Quorum(2), 'bls_signatures': Quorum(5), 'ledger_status_last_3PC': Quorum(2), 'observer_data': Quorum(2), 'ledger_status': Quorum(4), 'same_consistency_proof': Quorum(2), 'propagate': Quorum(2), 'backup_instance_faulty': Quorum(2), 'timestamp': Quorum(2), 'consisten
cy_proof': Quorum(2), 'view_change_done': Quorum(5), 'weak': Quorum(2), 'checkpoint': Quorum(4), 'f': 1, 'view_change': Quorum(5), 'strong': Quorum(5), 'n': 6, 'election': Quorum(5), 'commit': Quorum(5)}","Reachable_nodes":[["Node1",null],["Node2",null],["Node3",null],["
Node4",null]],"Reachable_nodes_count":4,"Read_only":false,"Suspicious_nodes":"","Total_nodes_count":6,"Unreachable_nodes":[["New_Node",null],["some",null]],"Unreachable_nodes_count":2,"f_value":1},"Protocol":{},"Software":{"Indy_packages":[""],"Installed_packages":["zipp
 0.5.2","yarl 1.3.0","wcwidth 0.1.7","ujson 1.33","typing 3.7.4","typing-extensions 3.7.4","timeout-decorator 0.4.0","supervisor 4.0.4","sortedcontainers 1.5.7","six 1.11.0","sha3 0.2.1","setuptools 28.8.0","semver 2.7.9","rlp 0.6.0","pyzmq 17.0.0","PyYAML 5.1.2","python
3-indy 1.10.1","python-rocksdb 0.6.9","python-dateutil 2.8.0","pytest 5.0.1","pyparsing 2.4.2","Pympler 0.5","Pygments 2.2.0","pycparser 2.19","pycares 3.0.0","py 1.8.0","psutil 5.4.3","prompt-toolkit 0.57","portalocker 0.5.7","pluggy 0.12.0","pip 9.0.3","pathlib2 2.3.4"
,"packaging 19.0","orderedset 2.0","multidict 4.5.2","msgpack-python 0.4.6","more-itertools 7.2.0","meld3 1.0.2","MarkupSafe 1.1.1","libnacl 1.6.1","leveldb 0.194","lazy-object-proxy 1.4.1","jsonpickle 0.9.6","Jinja2 2.10.1","ioflo 1.5.4","intervaltree 2.1.0","indy-plenu
m 1.9.0","indy-node 1.9.0","indy-anoncreds-dev 1.0.46","importlib-metadata 0.19","idna 2.8","idna-ssl 1.1.0","distro 1.3.0","Charm-Crypto 0.0.0","chardet 3.0.4","cffi 1.12.3","cchardet 2.1.4","base58 1.0.3","attrs 19.1.0","atomicwrites 1.3.0","async-timeout 3.0.1","aiosq
lite 0.10.0","aiohttp 3.5.4","aiohttp-jinja2 1.1.2","aiodns 2.0.0","indy-crypto 0.5.1"],"OS_version":"Linux-4.4.0-148-generic-x86_64-with-debian-stretch-sid","indy-node":"1.9.0","sovrin":"unknown"},"Update_time":"Wednesday, January 15, 2020 4:48:50 PM +0000","response-ve
rsion":"0.0.1","timestamp":1579106930},"identifier":"V4SGRU86Z58d6TV7PBUe6f","reqId":1579106872477556200,"type":"119"},
...
}
```

`validator-info`
- When run on a node in the pool, it provides information about the node's status.
- This is one of the first places to look if there are issues with the nodes on the ledger.
- If the nodes have not selected a 'primary' node

Example Output (run on a Node where the nodes have not selected a 'primary')
```
indy@72b147b1559e:~$ validator-info
Validator Node1 is in unknown state
Update time:     Thursday, January 16, 2020 9:08:52 PM +0000
Validator DID:    Gw6pDLhcBcoQesN72qfotTgFa7cbuqZpkX3Xo6pLhPhv
Verification Key: 33nHHYKnqmtGAVfZZGoP8hpeExeH45Fo8cKmd5mcnKYk7XgWNBxkkKJ
BLS Key: 4N8aUNHSgjQVgkpm8nhNEfDf6txHznoYREg9kirmJrkivgL4oSEimFF6nsQ6M41QvhM2Z33nves5vfSn9n1UwNFJBYtWVnHYMATn76vLuL3zU88KyeAYcHfsih3He6UHcXDxcaecHVz6                              jhCYz1P2UZn2bDVruL5wXpehgBfBaLKm3Ba
Node HA:        0.0.0.0:9701
Client HA:      0.0.0.0:9702
Metrics:
  Uptime: 32 minutes, 4 seconds
  Total audit Transactions:  156557
  Total pool Transactions:  6
  Total config Transactions:  0
  Total ledger Transactions:  8853
  Read Transactions/Seconds:  2.20
  Write Transactions/Seconds: 0.00
Reachable Hosts:   4/6
  Node3
  Node2
  Node4
  Node1
Unreachable Hosts: 2/6
  New_Node
  some
Software Versions:
  indy-node: 1.9.2
  sovrin: unknown
```

## Read Ledger
`read_ledger`
- When run on a node in the pool it provides information about the ledger.
- Note, when run on a node in a `von-network` instance you have to use `--base_dir` to redirect the command to use the pool data located in `/home/indy/ledger`.  Refer to the example below.

Examples:
```
read_ledger --type config --frm 24900
read_ledger --type pool --frm 1 --to 127 > /tmp/pool_ledger.txt
```

Example output when run on a `von-network` node:
```
indy@72b147b1559e:~$ read_ledger --type pool --frm 1 --to 127 --base_dir /home/indy/ledger
[1,{"reqSignature":{},"txn":{"data":{"data":{"alias":"Node1","blskey":"4N8aUNHSgjQVgkpm8nhNEfDf6txHznoYREg9kirmJrkivgL4oSEimFF6nsQ6M41QvhM2Z33nves5vfSn9n1UwNFJBYtWVnHYMATn76vLuL3zU88KyeAYcHfsih3He6UHcXDxcaecHVz6jhCYz1P2UZn2bDVruL5wXpehgBfBaLKm3Ba","blskey_pop":"RahHYiCvoNCtPTrVtP7nMC5eTYrsUA8WjXbdhNc8debh1agE9bGiJxWBXYNFbnJXoXhWFMvyqhqhRoq737YQemH5ik9oL7R4NTTCz2LEZhkgLJzB3QRQqJyBNyv7acbdHrAT8nQ9UkLbaVL9NBpnWXBTw4LEMePaSHEw66RzPNdAX1","client_ip":"159.203.21.90","client_port":9702,"node_ip":"159.203.21.90","node_port":9701,"services":["VALIDATOR"]},"dest":"Gw6pDLhcBcoQesN72qfotTgFa7cbuqZpkX3Xo6pLhPhv"},"metadata":{"from":"Th7MpTaRZVRYnPiabds81Y"},"type":"0"},"txnMetadata":{"seqNo":1,"txnId":"fea82e10e894419fe2bea7d96296a6d46f50f93f9eeda954ec461b2ed2950b62"},"ver":"1"}]
[2,{"reqSignature":{},"txn":{"data":{"data":{"alias":"Node2","blskey":"37rAPpXVoxzKhz7d9gkUe52XuXryuLXoM6P6LbWDB7LSbG62Lsb33sfG7zqS8TK1MXwuCHj1FKNzVpsnafmqLG1vXN88rt38mNFs9TENzm4QHdBzsvCuoBnPH7rpYYDo9DZNJePaDvRvqJKByCabubJz3XXKbEeshzpz4Ma5QYpJqjk","blskey_pop":"Qr658mWZ2YC8JXGXwMDQTzuZCWF7NK9EwxphGmcBvCh6ybUuLxbG65nsX4JvD4SPNtkJ2w9ug1yLTj6fgmuDg41TgECXjLCij3RMsV8CwewBVgVN67wsA45DFWvqvLtu4rjNnE9JbdFTc1Z4WCPA3Xan44K1HoHAq9EVeaRYs8zoF5","client_ip":"159.203.21.90","client_port":9704,"node_ip":"159.203.21.90","node_port":9703,"services":["VALIDATOR"]},"dest":"8ECVSk179mjsjKRLWiQtssMLgp6EPhWXtaYyStWPSGAb"},"metadata":{"from":"EbP4aYNeTHL6q385GuVpRV"},"type":"0"},"txnMetadata":{"seqNo":2,"txnId":"1ac8aece2a18ced660fef8694b61aac3af08ba875ce3026a160acbc3a3af35fc"},"ver":"1"}]
[3,{"reqSignature":{},"txn":{"data":{"data":{"alias":"Node3","blskey":"3WFpdbg7C5cnLYZwFZevJqhubkFALBfCBBok15GdrKMUhUjGsk3jV6QKj6MZgEubF7oqCafxNdkm7eswgA4sdKTRc82tLGzZBd6vNqU8dupzup6uYUf32KTHTPQbuUM8Yk4QFXjEf2Usu2TJcNkdgpyeUSX42u5LqdDDpNSWUK5deC5","blskey_pop":"QwDeb2CkNSx6r8QC8vGQK3GRv7Yndn84TGNijX8YXHPiagXajyfTjoR87rXUu4G4QLk2cF8NNyqWiYMus1623dELWwx57rLCFqGh7N4ZRbGDRP4fnVcaKg1BcUxQ866Ven4gw8y4N56S5HzxXNBZtLYmhGHvDtk6PFkFwCvxYrNYjh","client_ip":"159.203.21.90","client_port":9706,"node_ip":"159.203.21.90","node_port":9705,"services":["VALIDATOR"]},"dest":"DKVxG2fXXTU8yT5N7hGEbXB3dfdAnYv1JczDUHpmDxya"},"metadata":{"from":"4cU41vWW82ArfxJxHkzXPG"},"type":"0"},"txnMetadata":{"seqNo":3,"txnId":"7e9f355dffa78ed24668f0e0e369fd8c224076571c51e2ea8be5f26479edebe4"},"ver":"1"}]
[4,{"reqSignature":{},"txn":{"data":{"data":{"alias":"Node4","blskey":"2zN3bHM1m4rLz54MJHYSwvqzPchYp8jkHswveCLAEJVcX6Mm1wHQD1SkPYMzUDTZvWvhuE6VNAkK3KxVeEmsanSmvjVkReDeBEMxeDaayjcZjFGPydyey1qxBHmTvAnBKoPydvuTAqx5f7YNNRAdeLmUi99gERUU7TD8KfAa6MpQ9bw","blskey_pop":"RPLagxaR5xdimFzwmzYnz4ZhWtYQEj8iR5ZU53T2gitPCyCHQneUn2Huc4oeLd2B2HzkGnjAff4hWTJT6C7qHYB1Mv2wU5iHHGFWkhnTX9WsEAbunJCV2qcaXScKj4tTfvdDKfLiVuU2av6hbsMztirRze7LvYBkRHV3tGwyCptsrP","client_ip":"159.203.21.90","client_port":9708,"node_ip":"159.203.21.90","node_port":9707,"services":["VALIDATOR"]},"dest":"4PS3EDQ3dW1tci1Bp6543CfuuebjFrg36kLAUcskGfaA"},"metadata":{"from":"TWwCRQRZ2ZHMJFn9TzLp7W"},"type":"0"},"txnMetadata":{"seqNo":4,"txnId":"aa5e817d7cc626170eca175822029339a444eb0ee8f0bd20d3b0b76e566fb008"},"ver":"1"}]
[5,{"reqSignature":{"type":"ED25519","values":[{"from":"PcRTcn7S3gwjxER3FG3G3w","value":"vaKqXQgShSofhboy93fVDvTydguuJWX1aABV5oJLndcxW2s89KePZENqonfoLynUcorztwS44UCEFnfMdnPzFtN"}]},"txn":{"data":{"data":{"alias":"some","blskey":"4N8aUNHSgjQVgkpm8nhNEfDf6txHznoYREg9kirmJrkivgL4oSEimFF6nsQ6M41QvhM2Z33nves5vfSn9n1UwNFJBYtWVnHYMATn76vLuL3zU88KyeAYcHfsih3He6UHcXDxcaecHVz6jhCYz1P2UZn2bDVruL5wXpehgBfBaLKm3Ba","blskey_pop":"RahHYiCvoNCtPTrVtP7nMC5eTYrsUA8WjXbdhNc8debh1agE9bGiJxWBXYNFbnJXoXhWFMvyqhqhRoq737YQemH5ik9oL7R4NTTCz2LEZhkgLJzB3QRQqJyBNyv7acbdHrAT8nQ9UkLbaVL9NBpnWXBTw4LEMePaSHEw66RzPNdAX1","client_ip":"10.0.0.100","client_port":911,"node_ip":"10.0.0.100","node_port":910,"services":["VALIDATOR"]},"dest":"A5iWQVT3k8Zo9nXj4otmeqaUziPQPCiDqcydXkAJBk1Y"},"metadata":{"digest":"699a05837d8a5d34e65f0ef0087024683aa8aaf20dbf2a526098616c38854342","from":"PcRTcn7S3gwjxER3FG3G3w","payloadDigest":"ceefb68e99a30ec21dee6489d86205e61b04b2f93aca769a5e320d3e5418d717","reqId":1578857985619116000},"protocolVersion":2,"type":"0"},"txnMetadata":{"seqNo":5,"txnTime":1578857988},"ver":"1"}]
[6,{"reqSignature":{"type":"ED25519","values":[{"from":"3oWYuE2Q5ZvomJdgBZmogu","value":"52s4SuujVo8Gf22pfmAmxw96CniyNZTk8V8YyVGn6CBgbUDLB55E7gd9XNBn6CAyHmKHRceZspwHop8cFSePt8ZK"}]},"txn":{"data":{"data":{"alias":"New_Node","client_ip":"10.0.0.102","client_port":913,"node_ip":"10.0.0.101","node_port":912,"services":["VALIDATOR"]},"dest":"HyGpUThZu6kw2sFxcNTAoG23eCMK58W4vc3RACpjpSZD"},"metadata":{"digest":"297a0fc9c655a216acee048f5c2d3badcbafa12bd584140658f1b4a80fd95d94","from":"3oWYuE2Q5ZvomJdgBZmogu","payloadDigest":"52fe271c67a5796257f42eafbe71ca7351fbd5de9515ed9c59204f47fb680289","reqId":1578900314302208000},"protocolVersion":2,"type":"0"},"txnMetadata":{"seqNo":6,"txnTime":1578900318},"ver":"1"}]
```