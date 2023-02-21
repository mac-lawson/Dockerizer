import docker


'''
This function takes in the following parameters:

    image_name: The name of the Docker image to deploy.
    environment_vars: A dictionary containing environment variables to pass to the container.
    replicas: The number of container replicas to deploy.
    network_name: The name of the Docker network to deploy the container to.
    service_name: The name of the Docker service to create.

The function creates a Docker client using docker.from_env() and then specifies the container and deployment configurations using the provided parameters. It then creates the Docker service using client.services.create() and returns the ID of the created service.

You can call this function with the desired parameters to deploy your Docker containers to a production environment. Note that you will need to have access to a Docker engine or platform to run this function.
'''
def deploy_container(image_name, environment_vars, replicas, network_name, service_name):
    client = docker.from_env()

    container_config = {
        "image": image_name,
        "environment": environment_vars,
        "restart_policy": {
            "Name": "always"
        }
    }

    deployment_config = {
        "replicas": replicas,
        "endpoint_spec": {
            "Mode": "vip"
        }
    }

    service = client.services.create(
        name=service_name,
        task_template=container_config,
        networks=[network_name],
        mode=docker.types.ServiceMode("replicated", deployment_config),
    )

    print(f"Service created with ID: {service.id}")
