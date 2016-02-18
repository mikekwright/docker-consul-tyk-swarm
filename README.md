Docker Swarm Demo
=====================================

This repository is created to give you a system that you can use to test a docker cluster (setup using dockers supported swarm). 
To be able to use this repository you will need to have a virtualmachine setup that docker-machine can use to create its 
instances, this can be any of the below options:

    VirtualBox: virtualbox
    VMWare Fusion: vmwarefusion
    XHyve: xhyve

## Operations

There are 2 main operations that exist in the base script.  

    ./setup-cluster start

This operation will create a new cluster that is defined as one machine for hosting [consul](https://consul.io) (service discovery) 
after this machine has been created, 3 more machines are created for the swarm (one being the swarmmaster).   

The next operation is used to cleanup the environment.  

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

Once you have a cluster up and running you can start to deploy services to this cluster.  This can be accomplished by running the following
command.  

bash    

    eval $(docker-machine env --swarm swarmmaster)    

fish

    eval (docker-machine env --swarm swarmmaster) 

This will setup a connection so that all docker command will be run against the cluster and not against a single machine.  After this you just
need to run your `docker run` operation to get the new service up an running.   

    docker run -d -P --name webserver nginx

For each time you run this command the service will be registered and put together as a single service in consul.   

To view the consul page you will need to open a webpage to the consule ui, this can be done using the following command.    

bash

    open http://$(docker-machine ip consul):8500/ui

fish

    open http://(docker-machine ip consul):8500/ui

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


