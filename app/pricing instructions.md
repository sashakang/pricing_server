Build. Run from `/app` directory.

`docker build -t casts .`

# Run
Run container with binding `pwd`. Run from `docker` directory.

` docker run -v "$(pwd):\\SynologyDrive\\dikart\\pricing\\docker" -it --rm --name casts casts`

On server from `pricing` folder (ALSO WORKS FROM LOCAL CONTAINER from `app` folder):  

`docker run -v "$(pwd):/app" -it -p 8000:8000 --rm --name pricing sashakang/pricing`

Server responds with `ERR_EMPTY_RESPONSE`

Not sure about `-it` switch. Works without it at all.  
`-t` stands for pseudo-Putty, not relevant?  
`-i` may be relevant. Find it out.

`docker exec casts sh` doesn't work though.

# uvicorn
`uvicorn pricing_server:app --reload`

# Push

https://stackoverflow.com/questions/41984399/denied-requested-access-to-the-resource-is-denied-docker.  
TL&DR  
1. `docker logout`
2. `docker login`
3. `docker tag [source name] [acc name]/[image name]`  
	i.e. `docker tag casts sashakang/pricing`
4. `docker push sashakang/[image name]:[optional tag name]`  

This one seems to work:  
`cd app `  
`docker build -t casts .`  
`cd .. `  
or  
`docker build -t casts app`

then  
`docker run -v "$(pwd):/app" -it --rm --name casts casts`

Credentials stored in a separate `credentials` folder and are not pushed to `dockerhub`. Still need to confirm this.  
DB requests gets access to it and successfully executes the query.

### deamon not running error

Run `& 'c:\Program Files\Docker\Docker\DockerCli.exe' -SwitchDaemon` in pwsh in administrative mode.  
Then `Enable-WindowsOptionalFeature -Online -FeatureName $("Microsoft-Hyper-V", "Containers") -All` and restart.  
Should be all.

Alternatively  
```
Net stop com.docker.service
Net start com.docker.service
```  
and restart the client.

### Docker-compose  

No need for it yet.

### Next steps:  
- ~~run credentials from a file with docker~~
- ~~publish image @dockerhub without credentials~~
- ~~pull image to data server and run it ~~
- use volume, not mount