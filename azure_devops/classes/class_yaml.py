from ruamel.yaml import YAML

class Yaml:
    def __init__(
        self
        ,pool_name # Agent pool name.
        ,variable_group_name = None # Name of the Variable group from DevOps Library.
    ):
        self.yaml = YAML()
        self.yaml.preserve_quotes = True

        # Backbone of our YAML file
        self.yaml_data = {
            'trigger': ['main']
            ,'resources': [{'repo': 'self'}]
            ,'pool': {'name': pool_name}
        }

        if variable_group_name != None:
            self.yaml_data['variables'] = [{'group': variable_group_name}]

        self.yaml_data['stages'] = []


    def add_stage_push_to_acr(
        self
        ,image_repository # Name of the repository in ACR where we will push our image. If it doesn't exist it will be created.
        ,acr_service_connection_id # ID of a Service connection in DevOps linked to the ACR where we will be pushing image.
        ,tag # tag which we will add to the image in repository.
        ,dockerfile_path = '$(Build.SourcesDirectory)/Dockerfile'
    ):
        """
        Add stage for pushing a Docker image from repo to the ACR.
        """
        self.yaml_data['stages'].append({
            "stage": "Build"
            ,"displayName": "Build and push stage"
            ,"jobs": [{
                "job": "Build"
                ,"displayName": "Build and push an image to container registry"
                ,"steps": [
                    {
                        "task": "Docker@2"
                        ,"displayName": "Build and push an image to container registry"
                        ,"inputs": {
                            "command": "buildAndPush"
                            ,"repository": image_repository
                            ,"dockerfile": dockerfile_path
                            ,"containerRegistry": acr_service_connection_id
                            ,"tags": tag
                        }
                    }
                ]
            }]
        })


    def add_stage_deploy(
        self
        ,acr_name # Name of the ACR from which we will be pulling a Docker image (without '.azurecr.io')
        ,image_repository # Name of the repository in ACR with the image we want to pull
        ,tag # tag of the image from the image repository in ACR we want to pull
        ,docker_compose_path # path to the docker compose file relative to the root of the repo with code.
    ):
        """
        Add stage for pulling a Docker image from ACR to the Linux VM which is running an Agent. It is done by executing a bash script.
        """
        script = f"""
        - script: |
            image_name={acr_name}.azurecr.io/{image_repository}:{tag}

            # Set the Azure Pipeline variables as environment variables. They will be used in the docker-compose.yaml file.
            export CONTAINER_REGISTRY={acr_name}.azurecr.io
            export IMAGE_REPOSITORY={image_repository}
            export IMAGE_TAG={tag}

            # Below arguments SP_ID and SP_PASSWORD will be taken from the DevOps Library Variable group.
            echo "Login to Docker using service principal credentials"
            docker login {acr_name}.azurecr.io -u $(SP_ID) -p $(SP_PASSWORD)

            echo "Pulling the Docker image"
            docker pull $image_name

            echo "Running the Docker container"
            docker compose -f {docker_compose_path} up -d
        """

        self.yaml_data['stages'].append({
            "stage": "Deploy",
            "jobs": [{
                "job": "PullImage",
                "steps": [
                    {
                        "script": self.yaml.load(script)[0]['script']
                    }
                ]
            }]
        })


    def save(
        self
        ,file_path
    ):
        """
        Saving the YAML file in the given path.
        """
        with open(file_path, 'w') as f:
            self.yaml.dump(self.yaml_data, f)