import yaml

def generate_docker_compose(service_configs):
    """
    Generate a Docker Compose YAML file from a list of service configurations.

    Each service configuration is a dictionary containing the following keys:
    - name: The name of the service.
    - image: The Docker image to use for the service.
    - ports: A list of port mappings for the service.
    - volumes: A list of volume mappings for the service.
    - depends_on: A list of service names that this service depends on.
    """
    services = {}
    for service_config in service_configs:
        service_name = service_config['name']
        service = {
            'image': service_config['image'],
            'ports': service_config['ports'],
            'volumes': service_config['volumes'],
            'depends_on': service_config['depends_on']
        }
        services[service_name] = service

    compose_config = {'version': '3', 'services': services}

    return yaml.dump(compose_config)

# Example usage
service_configs = [
    {
        'name': 'web',
        'image': 'nginx:latest',
        'ports': ['80:80'],
        'volumes': ['./html:/usr/share/nginx/html'],
        'depends_on': ['api']
    },
    {
        'name': 'api',
        'image': 'my-api:latest',
        'ports': ['8000:8000'],
        'volumes': ['./data:/app/data'],
        'depends_on': ['db']
    },
    {
        'name': 'db',
        'image': 'mysql:latest',
        'ports': ['3306:3306'],
        'volumes': ['./db:/var/lib/mysql'],
        'depends_on': []
    }
]

docker_compose_yaml = generate_docker_compose(service_configs)
print(docker_compose_yaml)
