# Spook!
### The remote way to send a magic packet.

Spook is a project made for my own personal use, but I thought at least one other person might find this useful.

It serves a simple purpose - to sit on a network and send magic packets from a web UI.

It can be run either standalone, or as a Docker container hosted at 
[https://hub.docker.com/thebros35/spook](https://hub.docker.com/thebros35/spook). See the included 
`docker-compose.yml` file to set it up.

To run it from the command line: `docker run thebros35/spook -d -p 4321:8000 -p 9:9 -v spookVolume:/app/db 
--restart unless-stopped`

Usage is simple: enter a mac address into the Add field. The page will reload, and your entry will be saved in the 
embedded db. Then, hit send, and a magic packet will be sent to 255.255.255.255.

### Voilà! Your device is now on.

To build docker image, `docker build -t thebros35/spook .` and `docker push`.