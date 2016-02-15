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

