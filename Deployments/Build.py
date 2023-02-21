import os
import docker

'''
This script defines a function build_docker_image that takes the following parameters:

    image_name: the name and tag for the output Docker image
    dockerfile_path: the path to the Dockerfile used as a template for the custom image
    build_args: a dictionary containing build-time arguments used by the Dockerfile
    environment_vars: a dictionary containing environment variables used by the Docker build process

The function sets up the Docker client using docker.from_env(), sets the environment variables if provided, and then builds the Docker image using the client.images.build method. The pull and rm parameters ensure that the latest base image is pulled and that the intermediate containers are removed after the build is complete.
'''
def build_docker_image(image_name, dockerfile_path, build_args=None, environment_vars=None):
    client = docker.from_env()
    if build_args is None:
        build_args = {}
    if environment_vars is None:
        environment_vars = {}

    for key, value in environment_vars.items():
        os.environ[key] = value

    try:
        image = client.images.build(
            path=dockerfile_path,
            tag=image_name,
            buildargs=build_args,
            pull=True,
            rm=True
        )
        print(f"Image {image_name} created successfully.")
    except docker.errors.BuildError as e:
        print(f"Error building image {image_name}: {e}")
        return
