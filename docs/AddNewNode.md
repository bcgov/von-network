# Add new node



Guide to add new nodes for development purpose to VON-NETWORK Indy node network .



----



- [1. Modifying VON-NETWORK scripts/files](#1-modifying-von-network-scriptsfiles)

  - [1. Get DOCKERHOST IP](#1-get-dockerhost-ip)
  - [2. Scripts/Files](#2-scriptsfiles)
    - [von_generate_transactions](#von_generate_transactions)
    - [start_nodes.sh](#start_nodes.sh)
    - [docker-compose.yml](#docker-compose.yml)
    - [manage](#manage)
  - [3. Build container](#3-build-container)
  - [4. Start Ledger](#4-start-ledger)

- [2. Manually](#2-manually)

  - [TERMINAL_VON_NETWORK](#terminal_von_network)
    - [1. Start VON-NETWORK Ledger](#1-start-von-network-ledger)
    - [2. Manage logs](#2-manage-logs )
    - [3. Restart the ledger](#3-restart-the-ledger)
    
  - [TERMINAL_NODE_5](#terminal_node_5)
  
  - [TERMINAL_NODE_6](#terminal_node_6)
  
  - [TERMINAL_NODE_7](#terminal_node_7)
  
  - [TERMINAL_INDY_CLI](#terminal_indy_cli)
    - [1. Copy genesis files inside Nodes](#1-copy-genesis-files-inside-nodes)
    
    - [2. Register new Nodes in ledger](#2-register-new-nodes-in-ledger)
      - [1. Initialize the pool](#1-initialize-the-pool)
      - [2. Connect to pool](#2-connect-to-pool )
      - [3. Create wallet](#3-create-wallet)
      - [4. Create Trustee DID inside wallet](#4-create-trustee-did-inside-wallet)
      - [5. Create DIDs for Node[5,6,7] inside wallet](#5-create-dids-for-node567-inside-wallet)
      - [6. From DID Trustee register Node[5,6,7] DIDs as STEWARDS](#6-from-did-trustee-register-node567-dids-as-stewards)
      - [7. From each node DID register each NODE](#7-from-each-node-did-register-each-node)
      
  
- [Error loading transation data](#error-loading-transation-data)

- [References](#references)

  

----





We have two options to add nodes to Von-Network environment:

1. Modifying Von-Network scripts/files 
2. Manually.



## 1. Modifying VON-NETWORK scripts/files



This method does not give errors because all nodes are part of the genesis of the ledger.



### 1. Get DOCKERHOST IP

Get `Dockerhost` IP

```
USER@HOST:/von-network$ ./manage dockerhost

DockerHost: 192.168.65.3

USER@HOST:/von-network$
```



Create `VON_NETWORK/.env` file with the `Dockerhost` IP as many times as number of nodes (in our case seven times)

```
IP=192.168.65.3
IPS=192.168.65.3,192.168.65.3,192.168.65.3,192.168.65.3,192.168.65.3,192.168.65.3,192.168.65.3
```



> NOTE: Not able to pass IP and IPS like environment variables to scripts files. Used `export IP[s]=`



### 2. Scripts/Files

#### von_generate_transactions

Script locate at: `VON_NETWORK/bin/`



**Line 74**

Add new nodes IP.

From

```
    ipsArg="$ipAddress","$ipAddress","$ipAddress","$ipAddress"
```



To

```
    ipsArg="$ipAddress","$ipAddress","$ipAddress","$ipAddress","$ipAddress","$ipAddress","$ipAddress"
```



**Line 76**

Add new nodes IP.

From

```
    ipsArg="$DOCKERHOST","$DOCKERHOST","$DOCKERHOST","$DOCKERHOST"
```



To

```
    ipsArg="$DOCKERHOST","$DOCKERHOST","$DOCKERHOST","$DOCKERHOST","$DOCKERHOST","$DOCKERHOST","$DOCKERHOST"
```





**Lines 87 and 94**

Change from (4) to (7) number of nodes 

From

`  --nodes 4 \`

to

`  --nodes 7 \`



#### start_nodes.sh

Script locate at: `VON_NETWORK/scripts/`



**Line 7**

From

```
NODE_NUM="1 2 3 4"
```

To

```
NODE_NUM="1 2 3 4 5 6 7"
```



**Line 65**

Add the next blocks. Many blocks as number of nodes. Adjust ports for each node.

```
[program:node5]
command=start_indy_node Node5 $HOST 9709 $HOST 9710
directory=/home/indy
stdout_logfile=/tmp/node5.log
stderr_logfile=/tmp/node5.log

[program:node6]
command=start_indy_node Node5 $HOST 9711 $HOST 9712
directory=/home/indy
stdout_logfile=/tmp/node6.log
stderr_logfile=/tmp/node6.log

[program:node7]
command=start_indy_node Node5 $HOST 9713 $HOST 9714
directory=/home/indy
stdout_logfile=/tmp/node7.log
stderr_logfile=/tmp/node7.log
```



**Line 67**

Change the line to add new nodes logs.



From

```
command=tail -F /tmp/supervisord.log /tmp/node1.log /tmp/node2.log /tmp/node3.log /tmp/node4.log
```

To

```
command=tail -F /tmp/supervisord.log /tmp/node1.log /tmp/node2.log /tmp/node3.log /tmp/node4.log /tmp/node5.log /tmp/node6.log /tmp/node7.log
```





#### docker-compose.yml

Script locate at: `VON_NETWORK/`

**Line 92**

Add lines, two by each new nodes ports.

```
      - 9709:9709
      - 9710:9710
      - 9711:9711
      - 9712:9712
      - 9713:9713
      - 9714:9714
```



**Line 168**

Add next blocks. One by each new node

```
  node5:
    image: von-network-base
    command: 'bash -c ''./scripts/start_node.sh 5'''
    networks:
      - von
    ports:
      - 9709:9709
      - 9710:9710
    environment:
      - IP=${IP}
      - IPS=${IPS}
      - DOCKERHOST=${DOCKERHOST}
      - LOG_LEVEL=${LOG_LEVEL}
      - RUST_LOG=${RUST_LOG}
    volumes:
      - node5-data:/home/indy/ledger      

  node6:
    image: von-network-base
    command: 'bash -c ''./scripts/start_node.sh 6'''
    networks:
      - von
    ports:
      - 9711:9711
      - 9712:9712
    environment:
      - IP=${IP}
      - IPS=${IPS}
      - DOCKERHOST=${DOCKERHOST}
      - LOG_LEVEL=${LOG_LEVEL}
      - RUST_LOG=${RUST_LOG}
    volumes:
      - node6-data:/home/indy/ledger     

  node7:
    image: von-network-base
    command: 'bash -c ''./scripts/start_node.sh 7'''
    networks:
      - von
    ports:
      - 9713:9713
      - 9714:9714
    environment:
      - IP=${IP}
      - IPS=${IPS}
      - DOCKERHOST=${DOCKERHOST}
      - LOG_LEVEL=${LOG_LEVEL}
      - RUST_LOG=${RUST_LOG}
    volumes:
      - node7-data:/home/indy/ledger      

```



**Line 179**

Add new volumes. One for each new node

```
  node5-data:
  node6-data:
  node7-data:  
```



#### manage

Script locate at: `VON_NETWORK/`



**Line 407**

Add new nodes.

From

```
        -d webserver node1 node2 node3 node4
```

To

```
        -d webserver node1 node2 node3 node4 node5 node6 node7
```



**Line 436**

Add new nodes.

From

```
        -d synctest node1 node2 node3 node4
```

To

```
        -d synctest node1 node2 node3 node4 node5 node6 node7
```



### 3. Build container

We need to rebuild container to get inside `von-network-base` container image the modified sripts and files.

```
./manage rebuild
```



### 4. Start Ledger

```
USER@HOST:/von-network$ ./manage start
```



Congratulations you have a VON-NETWORK ledger with 7 nodes !



## 2. Manually

Von-Network enviroment (4 nodes) plus 3 containers (nodes) started with `von-network-base` image.

We need 5 terminals (TERMINAL_VON_NETWORK, TERMINAL_NODE_5, TERMINAL_NODE_6, TERMINAL_NODE_7 and TERMINAL_INDY_CLI) we are goning to do:

1. Start Containers, Initialize Nodes and start ledger Nodes in them.

2. Register new Nodes in ledger from Indy-cli.



We are going to move between terminals launching different commands. Be patient ;-)



### TERMINAL_VON_NETWORK

From von-network directory:

#### 1. Start VON-NETWORK Ledger

`USER@HOST:/von-network$./manage start`

When the environment is started check http://localhost:9000/ (if all  working fine we can see domain, pool and configuration ledgers and get genesis file).

From TERMINAL_NODE_[5,6,7] go to section `1. start the containers` and wait before start with `2. Node initialization`.



#### 2. Manage logs 

When Nodes are started (**AFTER** `1. Start the container` and `2. Node Initialization` in TERMINAL_NODE_[5,6,7]) 

`USER@HOST:/von-network$./manage logs`

We get the next messages in Node1, Node2, Node3 and Node4 logs.

```
node1_1      |WARNING|zstack.py|Node1 received message from unknown remote 3ouukk4hSmumojipxgoofs5JPZkASHWTrtJG5wfDPJQ7
node3_1      |WARNING|zstack.py|Node3 received message from unknown remote 3ouukk4hSmumojipxgoofs5JPZkASHWTrtJG5wfDPJQ7
node4_1      |WARNING|zstack.py|Node4 received message from unknown remote 3ouukk4hSmumojipxgoofs5JPZkASHWTrtJG5wfDPJQ7
node2_1      |WARNING|zstack.py|Node2 received message from unknown remote 3ouukk4hSmumojipxgoofs5JPZkASHWTrtJG5wfDPJQ7

node1_1      |WARNING|zstack.py|Node1 received message from unknown remote CPfw1xbhYjaPvdpgC5Q1hQNfBFoiPgUoUSTakPJ5mTmD
node3_1      |WARNING|zstack.py|Node3 received message from unknown remote CPfw1xbhYjaPvdpgC5Q1hQNfBFoiPgUoUSTakPJ5mTmD
node4_1      |WARNING|zstack.py|Node4 received message from unknown remote CPfw1xbhYjaPvdpgC5Q1hQNfBFoiPgUoUSTakPJ5mTmD
node2_1      |WARNING|zstack.py|Node2 received message from unknown remote CPfw1xbhYjaPvdpgC5Q1hQNfBFoiPgUoUSTakPJ5mTmD

node1_1      |WARNING|zstack.py|Node1 received message from unknown remote H6AmZrp7cA1gGshmRD6enB4mjN4Bh2FGZAxqKeBoBLyC
node3_1      |WARNING|zstack.py|Node3 received message from unknown remote H6AmZrp7cA1gGshmRD6enB4mjN4Bh2FGZAxqKeBoBLyC
node4_1      |WARNING|zstack.py|Node4 received message from unknown remote H6AmZrp7cA1gGshmRD6enB4mjN4Bh2FGZAxqKeBoBLyC
node2_1      |WARNING|zstack.py|Node2 received message from unknown remote H6AmZrp7cA1gGshmRD6enB4mjN4Bh2FGZAxqKeBoBLyC
```



That's because we haven't registered nodes in ledger so we do from [TERMINAL_INDY_CLI 2. Register new Nodes in ledger ](#2-register-new-nodes-in-ledger).



#### 3. Restart the ledger

When we have registered new Nodes in the ledger, from Ledger Browser we are able to see the new STEWARDS transactions when we are in DOMAIN browser, but in main dashboard only get initial 4 nodes  status.



`CTR+c` to exist from logs and

`USER@HOST:/von-network$./manage stop`



From TERMINAL_NODE_[5,6,7] go to section `4. Restart the node`  (no mather the order).



When new nodes are started.

`USER@HOST:/von-network$./manage start`



Now we are able to see in main dashboard 7 nodes  status.



### TERMINAL_NODE_5



[0. TERMINAL VON-NETWORK 1. Start VON-NETWORK Ledger](#1-start-von-network-ledger)



**1. Start the container**

```
USER@HOST:/von-network$ docker volume create von_node5-data
USER@HOST:/von-network$ docker run -ti -p 9709:9709 -p 9710:9710 --name von_node5_1 --network  von_von -v von_node5-data:/home/indy/ledger von-network-base /bin/bash
indy@CONTAINER_ID:~$
```

> NOTE: goto to [TERMINAL_INDY_CLI 1. Copy genesis files inside Nodes](#1-copy-genesis-files-inside-nodes)



**2. Node initialization**

`indy@CONTAINER_ID:~$ init_indy_keys --name Node5 --seed 000000000000000000000000000Node5`

```
Node-stack name is Node5
Client-stack name is Node5C
Generating keys for provided seed 000000000000000000000000000Node5
Init local keys for client-stack
Public key is 3ouukk4hSmumojipxgoofs5JPZkASHWTrtJG5wfDPJQ7
Verification key is 4SWokCJWJc69Tn74VvLS6t2G2ucvXqM9FDMsWJjmsUxe
Init local keys for node-stack
Public key is 3ouukk4hSmumojipxgoofs5JPZkASHWTrtJG5wfDPJQ7
Verification key is 4SWokCJWJc69Tn74VvLS6t2G2ucvXqM9FDMsWJjmsUxe
BLS Public key is 2JSLkTGhnG3ZzGoeuZufc7V1kF5wxHqTuSUbaudhwRJzsGZupNHs5igohLnsdcYG7kFj1JGC5aV2JuiJtDtHPKBeGw24ZmBJ44YYaqfCMi5ywNyP42aSjMkvjtHrGS7oVoFbP4aG4aRaKZL3UZbbGcnGTK5kfacmBNKdPSQDyXGCoxB
Proof of possession for BLS key is QkfRaLjoiQRyY5bmsJYRiDSvUrkVTHr671vTodMKTKTfKeVuawPLhGXk2few4bo5ZMC1LFMfHhaiMfJYPTzzJbdnWuZeucWcZjgcjAcBfg5GXSNUp2swExjju359MJLb1zQMoo2yFH3VCCkgtohHA1y5AbxAmzer4Rai2ndVHtyKoV
```



| key                             | Value                                                        |
| ------------------------------- | ------------------------------------------------------------ |
| Node-stack name                 | Node5                                                        |
| Client-stack  name              | Node5C                                                       |
| seed                            | 000000000000000000000000000Node5                             |
| Public key                      | 3ouukk4hSmumojipxgoofs5JPZkASHWTrtJG5wfDPJQ7                 |
| Verification key                | 4SWokCJWJc69Tn74VvLS6t2G2ucvXqM9FDMsWJjmsUxe                 |
| BLS PUBLIC Key                  | 2JSLkTGhnG3ZzGoeuZufc7V1kF5wxHqTuSUbaudhwRJzsGZupNHs5igohLnsdcYG7kFj1JGC5aV2JuiJtDtHPKBeGw24ZmBJ44YYaqfCMi5ywNyP42aSjMkvjtHrGS7oVoFbP4aG4aRaKZL3UZbbGcnGTK5kfacmBNKdPSQDyXGCoxB |
| Proof of possession for BLS key | QkfRaLjoiQRyY5bmsJYRiDSvUrkVTHr671vTodMKTKTfKeVuawPLhGXk2few4bo5ZMC1LFMfHhaiMfJYPTzzJbdnWuZeucWcZjgcjAcBfg5GXSNUp2swExjju359MJLb1zQMoo2yFH3VCCkgtohHA1y5AbxAmzer4Rai2ndVHtyKoV |



> NOTE: BEFORE 3. Start Node check that we have the files  /home/indy/ledger/sandbox/pool_transactions_genesis and  /home/indy/ledger/sandbox/domain_transactions_genesis inside this container.



**3. Start Node**

> NOTE: `start_indy_node NODE_NAME NODE_IP NODE_PORT CLIENT_IP CLIENT_PORT`

`indy@CONTAINER_ID:~/scripts$./start_node.sh 5`



When nodes start go to section [TERMINAL_VON_NETWORK 2. Manage logs](#2-manage-logs) 



**4. Restart the node**

CTR+c to stop the node. Wait to other nodes stop before start again.

`indy@CONTAINER_ID:~/scripts$./start_node.sh 5`



When Node started go to [TERMINAL VON-NETWORK 3. Restart the ledger](#3-restart-the-ledger) and finish starting VON-NETWORK.



### TERMINAL_NODE_6



[0. TERMINAL VON-NETWORK 1. Start VON-NETWORK Ledger](#1-start-von-network-ledger)



**1. Start the container**

```
USER@HOST:/von-network$ docker volume create von_node6-data
USER@HOST:/von-network$ docker run -ti -p 9711:9711 -p 9712:9712 --name von_node6_1 --network  von_von -v von_node6-data:/home/indy/ledger von-network-base /bin/bash
indy@CONTAINER_ID:~$
```

> NOTE: goto to  [TERMINAL_INDY_CLI 1. Copy genesis files inside Nodes](#1-copy-genesis-files-inside-nodes)



**2. Node initialization**

`indy@CONTAINER_ID:~$ init_indy_keys --name Node6 --seed 000000000000000000000000000Node6`

```
Node-stack name is Node6
Client-stack name is Node6C
Generating keys for provided seed 000000000000000000000000000Node6
Init local keys for client-stack
Public key is CPfw1xbhYjaPvdpgC5Q1hQNfBFoiPgUoUSTakPJ5mTmD
Verification key is Cv1Ehj43DDM5ttNBmC6VPpEfwXWwfGktHwjDJsTV5Fz8
Init local keys for node-stack
Public key is CPfw1xbhYjaPvdpgC5Q1hQNfBFoiPgUoUSTakPJ5mTmD
Verification key is Cv1Ehj43DDM5ttNBmC6VPpEfwXWwfGktHwjDJsTV5Fz8
BLS Public key is 3D5JAwAhjW5gik1ogKrnQaVrHY94e8E56iA5UifXjjYypMm2LifLiaRtgWJPiFA6uv2EiGy4MYByZ88Rmi8K3mUvb9TZeR9sdLBxsTdqrikeenac8ZVNkdCaFmGWcw8xVGqgv9cs574YDj7nuLHbJUDXN17J2fzQiD83iVQVQHW1RuU
Proof of possession for BLS key is RAMb2cWGE5K4VdTowDSCnTMi7bbHfLbELBL1XGWMSDgE5DMqGFgASmrrZnpqtyz9trDaf3VcE6LjyT72bHxR8ecPonBNUcuu5j3887C4RtVxPEkNjft2yZ2pMyYCXRiJ4bRmJMSvQa28xjXrTJ3wypzoeoa5DFA9Y6X8TLUe7hQLpP
```



| key                             | Value                                                        |
| ------------------------------- | ------------------------------------------------------------ |
| Node-stack name                 | Node6                                                        |
| Client-stack  name              | Node6C                                                       |
| seed                            | 000000000000000000000000000Node6                             |
| Public key                      | CPfw1xbhYjaPvdpgC5Q1hQNfBFoiPgUoUSTakPJ5mTmD                 |
| Verification key                | Cv1Ehj43DDM5ttNBmC6VPpEfwXWwfGktHwjDJsTV5Fz8                 |
| BLS PUBLIC Key                  | 3D5JAwAhjW5gik1ogKrnQaVrHY94e8E56iA5UifXjjYypMm2LifLiaRtgWJPiFA6uv2EiGy4MYByZ88Rmi8K3mUvb9TZeR9sdLBxsTdqrikeenac8ZVNkdCaFmGWcw8xVGqgv9cs574YDj7nuLHbJUDXN17J2fzQiD83iVQVQHW1RuU |
| Proof of possession for BLS key | RAMb2cWGE5K4VdTowDSCnTMi7bbHfLbELBL1XGWMSDgE5DMqGFgASmrrZnpqtyz9trDaf3VcE6LjyT72bHxR8ecPonBNUcuu5j3887C4RtVxPEkNjft2yZ2pMyYCXRiJ4bRmJMSvQa28xjXrTJ3wypzoeoa5DFA9Y6X8TLUe7hQLpP |



> NOTE: BEFORE 3. Start Node check that we have the files  /home/indy/ledger/sandbox/pool_transactions_genesis and  /home/indy/ledger/sandbox/domain_transactions_genesis inside this container.



**3. Start Node**

> NOTE: `start_indy_node NODE_NAME NODE_IP NODE_PORT CLIENT_IP CLIENT_PORT`

`indy@CONTAINER_ID:~/scripts$./start_node.sh 6`





When nodes start go to section [TERMINAL_VON_NETWORK 2. Manage logs](#2-manage-logs) 



**4. Restart the node**

CTR+c to stop the node. Wait to other nodes stop before start again.

`indy@CONTAINER_ID:~/scripts$./start_node.sh 6`



When Node started go to [TERMINAL VON-NETWORK 3. Restart the ledger](#3-restart-the-ledger) and finish starting VON-NETWORK.



### TERMINAL_NODE_7



[0. TERMINAL VON-NETWORK 1. Start VON-NETWORK Ledger](#1-start-von-network-ledger)



**1. Start the container**

```
USER@HOST:/von-network$ docker volume create von_node7-data
USER@HOST:/von-network$ docker run -ti -p 9713:9713 -p 9714:9714 --name von_node7_1 --network  von_von -v von_node7-data:/home/indy/ledger von-network-base /bin/bash
indy@CONTAINER_ID:~$
```

> NOTE: goto to  [TERMINAL_INDY_CLI 1. Copy genesis files inside Nodes](#1-copy-genesis-files-inside-nodes)



**2. Node initialization**

`indy@CONTAINER_ID:~$ init_indy_keys --name Node7 --seed 000000000000000000000000000Node7`

```
Node-stack name is Node7
Client-stack name is Node7C
Generating keys for provided seed 000000000000000000000000000Node7
Init local keys for client-stack
Public key is H6AmZrp7cA1gGshmRD6enB4mjN4Bh2FGZAxqKeBoBLyC
Verification key is BM8dTooz5uykCbYSAAFwKNkYfT4koomBHsSWHTDtkjhW
Init local keys for node-stack
Public key is H6AmZrp7cA1gGshmRD6enB4mjN4Bh2FGZAxqKeBoBLyC
Verification key is BM8dTooz5uykCbYSAAFwKNkYfT4koomBHsSWHTDtkjhW
BLS Public key is 4ahBpE7gVEhW2evVgS69EJeSyciwbbby67iQj4htsgdtCxxXsEHMS6oKVeEQvrBBgncHfAddQyTt7ZF1PcfMX1Gu3xsgnzBDcLzPBz6ZdoXwi3uDPEoDZHXeDp1AFj8cidhfBWzY1FfKZMvh1HYQX8zZWMw579pYs3SyNoWLNdsNd8Q
Proof of possession for BLS key is RSZqkPwZKyXxn4qwDNQ9m9hkqBbpdMCzz9pTobyxArnQbZiLkxFTStdGyDmwmyH7fRkXygyTp7ib4VJWeJitfDbZyv2yTr3ShbBWvYEkX7jGUZDdoS3EXYfAserSLsPEdL1U3Y9tuXRuEKd99VHhcem1sPop5mNn92ryKZGvv1auWP
```



| key                             | Value                                                        |
| ------------------------------- | ------------------------------------------------------------ |
| Node-stack name                 | Node7                                                        |
| Client-stack  name              | Node7C                                                       |
| seed                            | 000000000000000000000000000Node7                             |
| Public key                      | H6AmZrp7cA1gGshmRD6enB4mjN4Bh2FGZAxqKeBoBLyC                 |
| Verification key                | BM8dTooz5uykCbYSAAFwKNkYfT4koomBHsSWHTDtkjhW                 |
| BLS PUBLIC Key                  | 4ahBpE7gVEhW2evVgS69EJeSyciwbbby67iQj4htsgdtCxxXsEHMS6oKVeEQvrBBgncHfAddQyTt7ZF1PcfMX1Gu3xsgnzBDcLzPBz6ZdoXwi3uDPEoDZHXeDp1AFj8cidhfBWzY1FfKZMvh1HYQX8zZWMw579pYs3SyNoWLNdsNd8Q |
| Proof of possession for BLS key | RSZqkPwZKyXxn4qwDNQ9m9hkqBbpdMCzz9pTobyxArnQbZiLkxFTStdGyDmwmyH7fRkXygyTp7ib4VJWeJitfDbZyv2yTr3ShbBWvYEkX7jGUZDdoS3EXYfAserSLsPEdL1U3Y9tuXRuEKd99VHhcem1sPop5mNn92ryKZGvv1auWP |



> NOTE: BEFORE 3. Start Node check that we have the files  /home/indy/ledger/sandbox/pool_transactions_genesis and  /home/indy/ledger/sandbox/domain_transactions_genesis inside this container.



**3. Start Node**

> NOTE: `start_indy_node NODE_NAME NODE_IP NODE_PORT CLIENT_IP CLIENT_PORT`

`indy@CONTAINER_ID:~/scripts$./start_node.sh 7`



When nodes start go to section [TERMINAL_VON_NETWORK 2. Manage logs](#2-manage-logs) 



**4. Restart the node**

CTR+c to stop the node. Wait to other nodes stops before start again.

`indy@CONTAINER_ID:~/scripts$./start_node.sh 7`



When Node started go to [TERMINAL VON-NETWORK 3. Restart the ledger](#3-restart-the-ledger) and finish starting VON-NETWORK.





### TERMINAL_INDY_CLI



[0. TERMINAL VON-NETWORK 1. Start VON-NETWORK Ledger](#1-start-von-network-ledger)



From von-network directory:



#### 1. Copy genesis files inside Nodes

When containers are started (TERMINAL_NODE_[5,6,7] `1. Start the container`) from this terminal copy inside them `pool_transactions_genesis` and `domain_transactions_genesis`  files. Take them from one of the nodes to new ones and place in /home/indy/ledger/sandbox

f.e

```
USER@HOST:/von-network$ docker cp von_node1_1:/home/indy/ledger/sandbox/pool_transactions_genesis .
USER@HOST:/von-network$ docker cp von_node1_1:/home/indy/ledger/sandbox/domain_transactions_genesis .

USER@HOST:/von-network$ docker cp pool_transactions_genesis von_node[5,6,7]_1:/home/indy/ledger/sandbox/pool_transactions_genesis
USER@HOST:/von-network$ docker cp domain_transactions_genesis von_node[5,6,7]_1:/home/indy/ledger/sandbox/domain_transactions_genesis
```



Now in each TERMINAL_NODE_[5,6,7]  go to section `2. Node initialization` and then `3. Start Node` .



#### 2. Register new Nodes in ledger



1. Initialize the pool.
2. Connect to pool.
3. Create a wallet.
4. Create Trustee DID inside wallet.
5. Create DIDs for Node5, Node6 and Node7 inside wallet.
6. From DID trustee Register Node5, Node6 and Node7 DIDs as STEWARDS.
7. From each node DID register each NODE.



##### 1. Initialize the pool

> NOTE: you can get [$DOCKERHOST](#1-get-dockerhost-ip)

```
USER@HOST:./manage cli init-pool mylocalpool http://$DOCKERHOST:9000/genesis
Creating von_client_run ... done
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3092  100  3092    0     0   503k      0 --:--:-- --:--:-- --:--:--  503k

USER@HOST:./manage indy-cli
Creating von_client_run ... done
indy>
```



##### 2. Connect to pool 

We check that `mylocalpoll` has been created and we can connect to it.

```
indy> pool list
+-------------+
| Pool        |
+-------------+
| mylocalpool |
+-------------+
indy>
indy> pool connect mylocalpool
Pool "mylocalpool" has been connected
pool(mylocalpool):indy>
```



##### 3. Create wallet

Create a wallet giving a name (wtrustee) and key (f.e wtrusteekey).

Open the wallet.

```
pool(mylocalpool):indy> wallet create wtrustee key=wtrusteekey
Wallet "wtrustee" has been created
pool(mylocalpool):indy> wallet open wtrustee key=wtrusteekey
Wallet "wtrustee" has been opened
pool(mylocalpool):wtrustee:indy>
```



##### 4. Create Trustee DID inside wallet

**DID** (V4SGRU86Z58d6TV7PBUe6f) and **seed** (000000000000000000000000Trustee1) **MUST BE THESE**. Metadata is optional.

> NOTE: If you have your own network you need put your DID and seed for Trustee.



```
pool(mylocalpool):wtrustee:indy> did new did=V4SGRU86Z58d6TV7PBUe6f seed=000000000000000000000000Trustee1 metadata=trustee
Did "V4SGRU86Z58d6TV7PBUe6f" has been created with "~CoRER63DVYnWZtK8uAzNbx" verkey
Metadata has been saved for DID "V4SGRU86Z58d6TV7PBUe6f"
pool(mylocalpool):wtrustee:indy> did list
+------------------------+-------------------------+----------+
| Did                    | Verkey                  | Metadata |
+------------------------+-------------------------+----------+
| V4SGRU86Z58d6TV7PBUe6f | ~CoRER63DVYnWZtK8uAzNbx | trustee  |
+------------------------+-------------------------+----------+
pool(mylocalpool):wtrustee:indy>
```



##### 5. Create DIDs for Node[5,6,7] inside wallet

We use as DID the `Public key`  generated and `seed` used during `2. Node Initialization` of the NODE[5,6,7]



```
pool(mylocalpool):wtrustee:indy> did new did=3ouukk4hSmumojipxgoofs5JPZkASHWTrtJG5wfDPJQ7 seed=000000000000000000000000000Node5 metadata=node5
pool(mylocalpool):wtrustee:indy> did new did=CPfw1xbhYjaPvdpgC5Q1hQNfBFoiPgUoUSTakPJ5mTmD seed=000000000000000000000000000Node6 metadata=node6
pool(mylocalpool):wtrustee:indy> did new did=H6AmZrp7cA1gGshmRD6enB4mjN4Bh2FGZAxqKeBoBLyC seed=000000000000000000000000000Node7 metadata=node7
pool(mylocalpool):wtrustee:indy> did list
+----------------------------------------------+----------------------------------------------+----------+
| Did                                          | Verkey                                       | Metadata |
+----------------------------------------------+----------------------------------------------+----------+
| H6AmZrp7cA1gGshmRD6enB4mjN4Bh2FGZAxqKeBoBLyC | BM8dTooz5uykCbYSAAFwKNkYfT4koomBHsSWHTDtkjhW | node7    |
+----------------------------------------------+----------------------------------------------+----------+
| CPfw1xbhYjaPvdpgC5Q1hQNfBFoiPgUoUSTakPJ5mTmD | Cv1Ehj43DDM5ttNBmC6VPpEfwXWwfGktHwjDJsTV5Fz8 | Node6    |
+----------------------------------------------+----------------------------------------------+----------+
| 3ouukk4hSmumojipxgoofs5JPZkASHWTrtJG5wfDPJQ7 | 4SWokCJWJc69Tn74VvLS6t2G2ucvXqM9FDMsWJjmsUxe | node5    |
+----------------------------------------------+----------------------------------------------+----------+
| V4SGRU86Z58d6TV7PBUe6f                       | ~CoRER63DVYnWZtK8uAzNbx                      | trustee  |
+----------------------------------------------+----------------------------------------------+----------+
pool(mylocalpool):wtrustee:indy>
```



##### 6. From DID Trustee register Node[5,6,7] DIDs as STEWARDS

We use as DID the `Public key`  and `Verification key` for verkey generated during `2. Node Initialization` of the NODE[5,6,7]

The ROLE used is 2.

```
- None (common USER)
- “0” (TRUSTEE)
- “2” (STEWARD)
- “101” (ENDORSER)
- “201” (NETWORK_MONITOR)
```



```
pool(mylocalpool):wtrustee:indy> did use V4SGRU86Z58d6TV7PBUe6f
Did "V4SGRU86Z58d6TV7PBUe6f" has been set as active
pool(mylocalpool):wtrustee:did(V4S...e6f):indy> ledger nym did=3ouukk4hSmumojipxgoofs5JPZkASHWTrtJG5wfDPJQ7 verkey=4SWokCJWJc69Tn74VvLS6t2G2ucvXqM9FDMsWJjmsUxe role=2 send=true
pool(mylocalpool):wtrustee:did(V4S...e6f):indy> ledger nym did=CPfw1xbhYjaPvdpgC5Q1hQNfBFoiPgUoUSTakPJ5mTmD verkey=Cv1Ehj43DDM5ttNBmC6VPpEfwXWwfGktHwjDJsTV5Fz8 role=2 send=true
pool(mylocalpool):wtrustee:did(V4S...e6f):indy> ledger nym did=H6AmZrp7cA1gGshmRD6enB4mjN4Bh2FGZAxqKeBoBLyC verkey=BM8dTooz5uykCbYSAAFwKNkYfT4koomBHsSWHTDtkjhW role=2 send=true
pool(mylocalpool):wtrustee:indy>
```



##### 7. From each node DID register each NODE

To register NODEs use the information used and generated during `2. Node Initialization` of the NODE[5,6,7]

|             |                                                       |
| ----------- | ----------------------------------------------------- |
| target      | Verification key                                      |
| alias       | NodeX                                                 |
| node_ip     | DOCKERHOST IP [Get DOCKERHOST IP](#get-dockerhost-ip) |
| node_port   |                                                       |
| client_ip   | DOCKERHOST IP [Get DOCKERHOST IP](#get-dockerhost-ip) |
| client_port |                                                       |
| blskey      | BLS Public key                                        |
| blskey_pop  | Proof of possession for BLS key                       |



**Node5**

```
pool(mylocalpool):wtrustee:indy>
pool(mylocalpool):wtrustee:indy> did use 3ouukk4hSmumojipxgoofs5JPZkASHWTrtJG5wfDPJQ7
Did "3ouukk4hSmumojipxgoofs5JPZkASHWTrtJG5wfDPJQ7" has been set as active
pool(mylocalpool):wtrustee:did(3ou...JQ7):indy> ledger node target=4SWokCJWJc69Tn74VvLS6t2G2ucvXqM9FDMsWJjmsUxe alias=Node5 node_ip=192.168.65.3 node_port=9709 client_port=9710 client_ip=192.168.65.3 services=VALIDATOR blskey=2JSLkTGhnG3ZzGoeuZufc7V1kF5wxHqTuSUbaudhwRJzsGZupNHs5igohLnsdcYG7kFj1JGC5aV2JuiJtDtHPKBeGw24ZmBJ44YYaqfCMi5ywNyP42aSjMkvjtHrGS7oVoFbP4aG4aRaKZL3UZbbGcnGTK5kfacmBNKdPSQDyXGCoxB blskey_pop=QkfRaLjoiQRyY5bmsJYRiDSvUrkVTHr671vTodMKTKTfKeVuawPLhGXk2few4bo5ZMC1LFMfHhaiMfJYPTzzJbdnWuZeucWcZjgcjAcBfg5GXSNUp2swExjju359MJLb1zQMoo2yFH3VCCkgtohHA1y5AbxAmzer4Rai2ndVHtyKoV send=true
pool(mylocalpool):wtrustee:did(3ou...JQ7):indy>
```



**Node6**

```
pool(mylocalpool):wtrustee:did(3ou...JQ7):indy> did use CPfw1xbhYjaPvdpgC5Q1hQNfBFoiPgUoUSTakPJ5mTmD
Did "CPfw1xbhYjaPvdpgC5Q1hQNfBFoiPgUoUSTakPJ5mTmD" has been set as active
pool(mylocalpool):wtrustee:did(CPf...TmD):indy> ledger node target=Cv1Ehj43DDM5ttNBmC6VPpEfwXWwfGktHwjDJsTV5Fz8 alias=Node6 node_ip=192.168.65.3 node_port=9711 client_port=9712 client_ip=192.168.65.3 services=VALIDATOR 5JAwAhjW5gik1ogKrnQaVrHY94e8E56iA5UifXjjYypMm2LifLiaRtgWJPiFA6uv2EiGy4MYByZ88Rmi8K3mUvb9TZeR9sdLBxsTdqrikeenac8ZVNkdCaFmGWcw8xVGqgv9cs574YDj7nuLHbJUDXN17J2fzQiD83iVQVQHW1RuU  blskey_pop=RAMb2cWGE5K4VdTowDSCnTMi7bbHfLbELBL1XGWMSDgE5DMqGFgASmrrZnpqtyz9trDaf3VcE6LjyT72bHxR8ecPonBNUcuu5j3887C4RtVxPEkNjft2yZ2pMyYCXRiJ4bRmJMSvQa28xjXrTJ3wypzoeoa5DFA9Y6X8TLUe7hQLpP send=true
pool(mylocalpool):wtrustee:did(CPf...TmD):indy>
```



**Node7**

```
pool(mylocalpool):wtrustee:did(CPf...TmD):indy> did use H6AmZrp7cA1gGshmRD6enB4mjN4Bh2FGZAxqKeBoBLyC
Did "H6AmZrp7cA1gGshmRD6enB4mjN4Bh2FGZAxqKeBoBLyC" has been set as active
pool(mylocalpool):wtrustee:did(H6A...LyC):indy> ledger node target=BM8dTooz5uykCbYSAAFwKNkYfT4koomBHsSWHTDtkjhW alias=Node7 node_ip=192.168.65.3 node_port=9713 client_port=9714 client_ip=192.168.65.3 services=VALIDATOR blskey=4ahBpE7gVEhW2evVgS69EJeSyciwbbby67iQj4htsgdtCxxXsEHMS6oKVeEQvrBBgncHfAddQyTt7ZF1PcfMX1Gu3xsgnzBDcLzPBz6ZdoXwi3uDPEoDZHXeDp1AFj8cidhfBWzY1FfKZMvh1HYQX8zZWMw579pYs3SyNoWLNdsNd8Q  blskey_pop=RSZqkPwZKyXxn4qwDNQ9m9hkqBbpdMCzz9pTobyxArnQbZiLkxFTStdGyDmwmyH7fRkXygyTp7ib4VJWeJitfDbZyv2yTr3ShbBWvYEkX7jGUZDdoS3EXYfAserSLsPEdL1U3Y9tuXRuEKd99VHhcem1sPop5mNn92ryKZGvv1auWP send=true
````

After that in TERMINAL_NODE5, TERMINAL_NODE6 and TERMINAL_NODE7 the nodes start synching, wait until synch finish.



When synch fish go to [TERMINAL VON-NETWORK 3. Restart the ledger](#3-restart-the-ledger).







## Error loading transation data



When we add new nodes [manually](#2-manually) from Ledgder Browser we can see 7 Nodes status, but when we go to POOL ledger we get `Error loading transation data`.

I' have tried to star Ledger Browser with `Where LEDGER_SEED is set to a SEED that has permissions to read the pool ledger. Must have a Network Monitor or higher role.`

./manage start-web --logs GENESIS_URL=https://WEBSERVER/genesis/genesis.txn LEDGER_SEED=000000000000000000000000Trustee1

And the error in logs when acces to POOL ledger is:

```
webserver_1  | 2021-06-29 16:15:58,076|DEBUG|core.py|returning None
webserver_1  | 2021-06-29 16:15:58,076|ERROR|web_protocol.py|Error handling request
webserver_1  | Traceback (most recent call last):
webserver_1  |   File "/home/indy/.pyenv/versions/3.6.9/lib/python3.6/site-packages/aiohttp/web_protocol.py", line 418, in start
webserver_1  |     resp = await task
webserver_1  |   File "/home/indy/.pyenv/versions/3.6.9/lib/python3.6/site-packages/aiohttp/web_app.py", line 458, in _handle
webserver_1  |     resp = await handler(request)
webserver_1  |   File "/home/indy/server/server.py", line 157, in ledger_json
webserver_1  |     last_modified = max(last_modified, row[1]) if last_modified else row[1]
webserver_1  | TypeError: '>' not supported between instances of 'NoneType' and 'str'
webserver_1  | 2021-06-29 16:15:58,079|INFO|web_log.py|172.20.0.1 [29/Jun/2021:16:15:58 +0000] "GET /ledger/pool?page=1&page_size=10&query=&type= HTTP/1.1" 500 244 "http://localhost:9000/browse/pool" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
webserver_1  | 2021-06-29 16:17:01,649|DEBUG|anchor.py|Resyncing ledger cache: POOL
```



Reviewing Ledger Browser logs when clicking in Domain Ledger and in Pool Ledger and the server.py file at line 157 

`last_modified = max(last_modified, row[1]) if last_modified else row[1]`

the problem was when the **last_modified**  has a `txId(str)` and **row[1]**  `None`.



|                                                              |       |
| ------------------------------------------------------------ | ----- |
| None > None                                                  | OK    |
| None > '60793029607b93c585a2cae0b9c5a2646c5450772c4534ee7dde764c3891a5d6' | OK    |
| 'aa5e817d7cc626170eca175822029339a444eb0ee8f0bd20d3b0b76e566fb008'  > None | ERROR |



To solve the problem we catch the exception `TypeError: '>' not supported between instances of 'NoneType' and 'str'` in `server.py` file change 

File locate at: `VON_NETWORK/server/server.py`

**Line 157**

From

```
        last_modified = max(last_modified, row[1]) if last_modified else row[1]
```

To

```
        try:
            last_modified = max(last_modified, row[1]) if last_modified else row[1]
        except TypeError:
            last_modified = row[1]
```







## References



https://hyperledger-indy.readthedocs.io/projects/node/en/latest/add-node.html





