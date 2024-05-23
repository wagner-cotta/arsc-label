import json
import os

import requests


class APIRequest:
    """
    A class to interact with the GitHub API for managing
    labels on issues or pull requests.

    Dependencies:
    requests: To make HTTP requests to the GitHub API.

    Attributes:
        api_version (str): The GitHub API version.
        owner (str): The owner of the GitHub repository.
        repository (str): The name of the GitHub repository.
        token (str): The GitHub API token for authorization.
        obj_id (int): The ID of the issue or pull request to manage labels for.
        url_prefix (str): The URL prefix for GitHub API requests.
        url_suffix (str): The URL suffix for GitHub API requests
        specific to labels.

    Methods:
        get_headers(request_type):
            Generates headers for the API request based on the request type.

        get_labels_from_obj(obj="repository"):
            Retrieves labels from the specified object type.
            (For future development)

        get_a_label(name):
            Retrieves information about a specific label by name.
            (For future development)

        add_labels_to_obj(labels):
            Adds labels to the specified object.

        set_label_to_obj(labels):
            Sets labels on the specified object, replacing existing ones.

        label_to_data(labels):
            Converts a comma-separated string of labels into the
            required JSON format.

        remove_label_from_obj(label):
            Removes a specific label from the specified object.

        clear_labels_from_obj():
            Removes all labels from the specified object.

        do_request(url_prefix, url_suffix, request_type, data=None):
            Executes the HTTP request with the given parameters.
    """

    def __init__(
        self,
        api_version="",
        owner="",
        repository="",
        token="",
        obj_id=0,
    ):
        self.obj_id = obj_id
        self.token = token
        self.api_version = api_version
        self.url_prefix = f"https://api.github.com/repos/{owner}/{repository}"
        self.url_suffix = f"/issues/{self.obj_id}/labels"

    def get_headers(self, request_type):
        """
        Generates headers for the API request based on the request type.

        Parameters:
            request_type (str): The type of HTTP request
            (GET, POST, PUT, DELETE).

        Returns:
            dict: The headers required for the API request.
        """
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": f"{self.api_version}",
        }
        if request_type in ("POST", "PUT"):
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        return headers

    def get_labels_from_obj(self, obj="repository"):
        """
        Retrieves labels from the specified object type.

        Parameters:
            obj (str): The type of object to retrieve labels from
            (repository, issue, pull_request).

        Returns:
            Response: The response from the GitHub API.
        """
        if obj == "repository":
            suffix = self.url_suffix
        elif obj in ("issue", "pull_request"):
            suffix = "/labels"
        else:
            return "Invalid obj type"
        return self.do_request(self.url_prefix, suffix, "GET")

    def get_a_label(self, name):
        """
        Retrieves information about a specific label by name.

        Parameters:
            name (str): The name of the label to retrieve.

        Returns:
            Response: The response from the GitHub API.
        """
        suffix = f"/labels/{name}"
        return self.do_request(self.url_prefix, suffix, "GET")

    def add_labels_to_obj(self, labels):
        """
        Adds labels to the specified object.

        Parameters:
            labels (str): A comma-separated string of labels to add.

        Returns:
            Response: The response from the GitHub API.
        """
        return self.do_request(
            self.url_prefix,
            self.url_suffix,
            "POST",
            data=self.label_to_data(labels),
        )

    def set_label_to_obj(self, labels):
        """
        Sets labels on the specified object, replacing existing ones.

        Parameters:
            labels (str): A comma-separated string of labels to set.

        Returns:
            Response: The response from the GitHub API.
        """
        return self.do_request(
            self.url_prefix,
            self.url_suffix,
            "PUT",
            data=self.label_to_data(labels),
        )

    def label_to_data(self, labels):
        """
        Converts a comma-separated string of labels
        into the required JSON format.

        Parameters:
            labels (str): A comma-separated string of labels.

        Returns:
            str: The JSON string representing the labels.
        """
        labels = labels.replace(" ", "").split(",")
        labels_str = '","'.join(labels)
        result_str = f'{{"labels":["{labels_str}"]}}'
        return result_str

    def remove_label_from_obj(self, label):
        """
        Removes a specific label from the specified object.

        Parameters:
            label (str): The name of the label to remove.

        Returns:
            Response: The response from the GitHub API.
        """
        suffix = f"/issues/{self.obj_id}/labels/{label}"
        return self.do_request(self.url_prefix, suffix, "DELETE")

    def clear_labels_from_obj(self):
        """
        Removes all labels from the specified object.

        Returns:
            Response: The response from the GitHub API.
        """
        return self.do_request(self.url_prefix, self.url_suffix, "DELETE")

    def do_request(self, url_prefix, url_suffix, request_type, data=None):
        """
        Executes the HTTP request with the given parameters.

        Parameters:
            url_prefix (str): The prefix of the URL for the request.
            url_suffix (str): The suffix of the URL for the request.
            request_type (str): The type of HTTP
            request (GET, POST, PUT, DELETE).
            data (str, optional): The data to include in the request body.

        Returns:
            Response: The response from the GitHub API.
        """
        if request_type == "POST":
            response = requests.post(
                f"{url_prefix}{url_suffix}",
                headers=self.get_headers("POST"),
                data=data,
                timeout=20,
            )
        if request_type == "PUT":
            response = requests.put(
                f"{url_prefix}{url_suffix}",
                headers=self.get_headers("PUT"),
                data=data,
                timeout=20,
            )
        if request_type == "DELETE":
            response = requests.delete(
                f"{url_prefix}{url_suffix}",
                headers=self.get_headers("DELETE"),
                timeout=5,
            )
        if request_type == "GET":
            response = requests.get(
                f"{url_prefix}{url_suffix}",
                headers=self.get_headers("GET"),
                timeout=20,
            )
        return response


def set_action_output(value):
    """Sets the GitHub Action output.

    Keyword arguments:
    output_name - The name of the output
    value - The value of the output
    """
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
            print(f"response={value}", file=f)


def main():
    """
    Main function to read GitHub API configuration
    from the environment, verify variables, and create an APIRequest instance.

    Reads the following variables from the environment variable 'GITHUB_ENV':
        - api: The GitHub API version.
        - owner: The owner of the GitHub repository.
        - repository: The name of the GitHub repository.
        - token: The GitHub API token for authorization.
        - obj_id: The ID of the issue or pull request to manage labels for.

    Raises:
        ValueError: If any of the required variables are missing.
    """
    supported_operations = {
        "add": "add_labels_to_obj",
        "remove": "remove_label_from_obj",
        "set": "set_label_to_obj",
        "clear": "clear_labels_from_obj",
    }
    try:
        api = os.environ.get("api")
        owner = os.environ.get("owner")
        repository = os.environ.get("repository")
        token = os.environ.get("token")
        obj_id = os.environ.get("obj_id")
        operation = os.environ.get("operation")
        labels = os.environ.get("labels")

        if not api:
            raise ValueError("The 'api' variable is missing from GITHUB_ENV")

        if not owner:
            raise ValueError("The 'owner' variable is missing from GITHUB_ENV")
        if not repository:
            raise ValueError(
                "The 'repository' variable is missing from GITHUB_ENV"
            )
        if not token:
            raise ValueError("The 'token' variable is missing from GITHUB_ENV")
        if not obj_id:
            raise ValueError(
                "The 'obj_id' variable is missing from GITHUB_ENV"
            )
        if not operation:
            raise ValueError(
                "The 'operation' variable is missing from GITHUB_ENV"
            )
        if operation not in supported_operations:
            raise ValueError(
                f"Unsupported operation: {operation}."
                f"Supported operations are: {supported_operations.keys()}"
            )

        if operation != "clear" and not labels:
            raise ValueError(
                "The 'labels' variable is missing from GITHUB_ENV"
            )

        api_request = APIRequest(
            owner=owner,
            repository=repository,
            token=token,
            obj_id=obj_id,
        )

        operation_method = getattr(
            api_request, supported_operations[operation]
        )

        set_action_output(
            operation_method(labels) if labels else operation_method()
        )

    except Exception as e:
        raise ValueError(f"An error occurred: {e}") from e


if __name__ == "__main__":
    main()
