# uvicorn
`uvicorn pricing_server:app --reload`

# Build

From `app` folder:  
`docker build -t sashakang/pricing .`  

or from `docker` folder:
`docker build -t sashakang/pricing app`

# Run

`docker run -v "$(pwd)/credentials:/credentials" -it --rm sashakang/pricing`

Credentials stored in a separate `credentials` folder and are not pushed to `dockerhub`.   
DB requests gets access to it and successfully executes the query.

## Run using container

Local container files stored in  
`\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\pricing-vol\_data\`.  
Copy `credentials` folder contents there.

Run using volume:  
`docker run -v pricing-vol:/credentials -it -p 8000:8000 --rm sashakang/pricing`

# Push

If access denied logout then login:

https://stackoverflow.com/questions/41984399/denied-requested-access-to-the-resource-is-denied-docker.  
TL&DR  
1. *optional* `docker logout`
2. *optional* `docker login`
3. *optional* `docker tag [source name] [acc name]/[image name]`,  
	i.e. `docker tag casts sashakang/pricing`.
4. `docker push sashakang/[image name]:[optional tag name]`,  
   i.e. `docker push sashakang/pricing`.

# `deamon not running error`

Run `& 'c:\Program Files\Docker\Docker\DockerCli.exe' -SwitchDaemon` in pwsh in administrative mode.  
Then `Enable-WindowsOptionalFeature -Online -FeatureName $("Microsoft-Hyper-V", "Containers") -All` and restart.  
Should be all.

Alternatively  
```
Net stop com.docker.service
Net start com.docker.service
```  
and restart the client.

# Docker-compose  

No need for it yet.

# Volume

Create a volume:  
`docker volume create analytics-vol`.

On Windows docker volume data location (type in file browser):  
`\\wsl$\docker-desktop-data\version-pack-data\community\docker\volumes\[volume_name]\_data\`.