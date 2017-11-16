# Tools

## bcovrin

Use `bcovrin` to easily run a pool of Indy nodes on a server.

1. Make sure your server allows inbound TCP traffic on ports 9701-9708.

2. Install docker:

```bash
curl -fsSL get.docker.com -o get-docker.sh
sh get-docker.sh
```

3. Download the script and make it executable:

```bash
curl https://raw.githubusercontent.com/nrempel/von-network/master/bin/bcovrin > bcovrin
chmod +x bcovrin
```

4. Create the docker container:

```bash
./bcovrin create
```

5. Start node cluster:

```bash
./bcovrin start
```

6. Stream the logs from the indy nodes:

```bash
./bcovrin logs
```

7. Running the CLI locally supports connecting to a remote node pool. Run on your local machine:

```bash
./manage cli <remote_ip>
```
