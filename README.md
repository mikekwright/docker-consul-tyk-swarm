Docker - Consul - Tyk
=====================================

I have updated this repository to be a demonstration of a docker swarm that uses a few tools together to deliver a simple
load balanced solution.  It uses the following technologies:    

1. Docker   
2. Docker Machine   
3. Docker Swarm   
4. [Consul](http://consul.io)   
5. [Registrator](http://gliderlabs.com/registrator/latest/)    
6. [Tyk](https://tyk.io/)    

To give you the most details I can about this system I will go over how to stand it up, how all the pieces interact and 
how the final product will perform.   

## System setup

This repository is created to give you a system that you can use to test a docker cluster (setup using dockers supported swarm). 
To be able to use this repository you will need to have a virtualmachine setup that docker-machine can use to create its 
instances, this can be any of the below options:

    VirtualBox: virtualbox
    VMWare Fusion: vmwarefusion
    XHyve: xhyve

## Operations

There are 2 main operations that exist in the base script.  

    ./setup-cluster start

This operation will create a docker machine that has a consul service used to track the swarm nodes and other nodes added to the
swarm.  This consul service can be opened by running `open http://$(docker-machine ip consul):8500/`.  It will then create a docker
swarm that consists of 3 nodes: `swarmmaster`, `swarms11`, `swarms2`.  This swarm has the `swarmmaster` node as the swarm master 
(yeah I know, figured I would call it out anyways).  This swarm is created using an overlay network which means all boxes should
have an address 10.0.0.x that they can use to communicate with each other.  After creating the swarm it will then install `consul` 
onto every node to actas the service discovery for each service (and dns on the boxes).  Then it installs `registrator` onto each
of the nodes to have them automatically register the started services with `consul`. Finally it will stand up the services necessary
for tyk to run which include: `redis`, `mongo`, `tyk_gateway` and `tyk_dashboard`.   

Once you are finished with a cluster you can free up the machines and destroy everything by running the below command: 

    ./setup-cluster stop

### Options

The default driver that will be used is virtualbox, however if you would like to use vmware or xhyve just use the below examples. 

bash 

    DOCKER_MACHINE_DRIVER=vmwarefusion ./setup-cluster start
    DOCKER_MACHINE_DRIVER=xhyve ./setup-cluster start

fish 

    env DOCKER_MACHINE_DRIVER=vmwarefusion ./setup-cluster start
    env DOCKER_MACHINE_DRIVER=xhyve ./setup-cluster start

## Use

So now you have the cluster running, lets go through a few commands to see how utilize this swarm cluster.   

### Connect to swarm

Once you have a cluster up and running you can start to deploy services to this cluster.  This can be accomplished by running the following
command.  

bash    

    eval $(docker-machine env --swarm swarmmaster)    

fish

    eval (docker-machine env --swarm swarmmaster) 

### Standup Webapp

This will setup a connection so that all docker command will be run against the cluster and not against a single machine.  After this you just
need to run your `docker run` operation to get the new service up an running. For our example we have a flask app that has been included 
in the repository so just un the following commands.  

    cd webapp/
    docker-compose up -d
    docker-compose scale flaskapp=3

We have created our simple webservice and scaled it to 3 instances.  To see these all running, you just need to run the below command.  

    docker ps

### View in Consul

Since this new service will automatically be registered to consul by `registrator` so we should be able to see this in the `consul`
ui which can be opened by running the following command:  

    open http://$(docker-machine ip swarmmaster):8500/ui

We can also see the results of this service using the consul http api by running the curl command listed below.  

    curl http://$(docker-machine ip swarmmaster):8500/v1/catalog/service/webapp_flaskapp

We need this endpoint to return the list of services that we started (since we spun up 3 there should be 3 that are returned).   

### Setup Tyk

Now we have our new webapp registered as a service in consul, we can use tyk to be our api frontend and have a custom endpoint forward to
our webapp.  

The first thing you will need to do is to login to the tyk dashboard portal.  The portal address and the username, password should have been
at the end of the output from `./setup-cluster start`.  Right now the username defaults to `test@test.com` and the password defaults to `changeme3`.  

Once you have the portal open you will want to click on the `Apis` link that is under the `System Management` section.   

Next click on the `Add new API` button that can be found on the upper right of the page.   

You should now be in the `API Designer` page.  At this point you will want to fill out the form providing an `API Name` and a corresponding `Listen Path`. 
(Note: the listen path should be automatically matched to the `API Name`).  You will also want to fill in the `Target URL`.  If you are planning to use
the service discovery feature (through consul) then you will want the `Target URL` to be `/`.  

If you are going to use service discovery then click on the checkbox next to `Enable service discovery` in the section `Service Discovery`.  To make
this work with consul you will need to fill in the `Query Endpoint` with a url similar to the one below.  

        http://x.x.x.x:8500/v1/catalog/service/webapp_flask

**Note: If you need to get the ip address you can get it by running `docker-machine ip swarmmaster`**      

Click the checkbox next to the entry `Does this endpoint return a list?`.  In the `Data path` field you want to put `ServiceAddress`.  Click on the 
checkbox next to `Is port information separate from the hostname?`, and then in the `Port data path:` field you want to put `ServicePort`.   

Finally in the `Target Details` section you will want to change the `Authentication Mode` to be `Open (keyless)`.   

Click on the `Save` button which can be found at the upper right of the page and that will have created a new api.   

To use this api you will want to go through the tyk_gateway.  The gateway ip should have been printed out with the tyk_dashboard login details.  
To test out our new service open curl and run the following command.   

        curl http://x.x.x.x:8080/<API Name>/

## Issues

There is a possibility that if you have used vagrant on you machine before then docker-machine will have problems with virtualbox, as vagrant
seems to disable the DHCP server option of the host-only network.  More info can be found [here](https://github.com/docker/toolbox/issues/273#issuecomment-171155241)    

## References

There are a number of great references that exist online that I used when going through this process including those listed below.  

* [Running a small docker swarm cluster](http://blog.scottlowe.org/2015/03/06/running-own-docker-swarm-cluster/)    
* [Docker - Evaluate Swarm in a sandbox](https://docs.docker.com/swarm/install-w-machine/)    
* [Docker Swarm cluster using Consul](http://blog.arungupta.me/docker-swarm-cluster-using-consul/)   
* [Docker DNS & Service Discovery with Consul and Registrator](http://artplustech.com/docker-consul-dns-registrator/)    
* [Consul Service Discovery with Docker](http://progrium.com/blog/2014/08/20/consul-service-discovery-with-docker/)  
* [Fun with Docker Swarm](https://www.safaribooksonline.com/blog/2015/11/17/fun-with-docker-swarm/)    
* [Tyk general documentation](https://tyk.io/v1.9/about/)    
* [Tyk Docker Setup](https://tyk.io/v1.8/setup/docker/)    
* [Tyk quickstart](https://gist.github.com/lonelycode/4f645c4733faaa74d8fd)    

