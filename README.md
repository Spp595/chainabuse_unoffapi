# UnOfficial ChainAbuse api

## Usage
```shell
curl -X POST "http://localhost:8000/checkwallet" \
  -H "Content-Type: application/json" \
  -d '{"value":"WALLET_ADDRESS"}'

➜  ~ {"reports":"1","types":["NFT Airdrop Scam 1"]}
```

## Run

```shell
docker run -d -p 8000:8000 \
  ghcr.io/spp595/chainabuse_unoffapi

```

## Run with proxy

```shell
docker run -d -p 8000:8000 \
  -e PROXY_HOST="host" \
  -e PROXY_USER="user" \
  -e PROXY_PASS="pass" \
  ghcr.io/spp595/chainabuse_unoffapi

```

## Docker Compose
```yaml
version: "3.7"
services:
  tgalertbot:
    image: ghcr.io/spp595/chainabuse_unoffapi
    restart: unless-stopped
    ports:
      - 8000:8000
    environment: # if need proxy
      PROXY_HOST: "host"
      PROXY_PASS: "pass"
      PROXY_USER: "user" 
```

## Build

```bash
git clone https://github.com/Spp595/chainabuse_unoffapi.git

cd chainabuse_unoffapi

docker build --rm --tag chainabuse_unoffapi:latest .

```
