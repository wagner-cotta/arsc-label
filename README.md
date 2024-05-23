# Add Remove Set Clear Label (ARSC Label)

------

The `arsc_label` action is designed to manage labels on issues or pull requests using the GitHub API. This action supports adding, removing, setting, and clearing labels based on configurations provided in the workflow.

#### Usage

To use `arsc_label` in your workflow, you need to configure the action accordingly.

#### Variables

The action reads its configuration from the input. These variables should be set in your GitHub Actions workflow.

| Variable   | Description                                               | Default                        |
| ---------- | --------------------------------------------------------- | ------------------------------ |
| api        | (Optional) The GitHub API version to use.                 | "2022-11-28"                   |
| owner      | (Optional) The owner of the GitHub repository.            | `github.repository_owner`      |
| repository | (Optional) The name of the GitHub repository.             | `github.event.repository.name` |
| token      | The GitHub API token for authorization.                   | (No default, must be provided) |
| obj_id     | The ID of the issue or pull request to manage labels for. | (No default, must be provided) |
| labels (1) | The labels to add, remove, or set.                        | (No default, must be provided) |
| operation  | The operation to perform. Supported operations are:       | (No default, must be provided) |

##### Operation:
| Operation | Description                          |
| --------- | ------------------------------------ |
| `add`     | Add labels.                          |
| `remove`  | Remove a label.                      |
| `set`     | Set labels, replacing existing ones. |
| `clear`   | Clear all labels.                    |

<font size="2">(1) For the operation that requires the `labels` inputm it should be provided as a comma-separated list of labels. If not provided, all labels will be removed. This is GitHub API default behavior and you can check it [here](https://docs.github.com/en/rest/issues/labels?apiVersion=2022-11-28).</font>

#### Workflow Example

```yaml
name: ARSC Label Example
on:
  workflow_dispatch:
    inputs:
      obj-id:
        description: "Issue/Pull Request Number"
        required: true
      operation:
        description: "Type"
        required: true
        type: choice
        options: ["add", "remove", "set", "clear"]
      labels:
        description: "Labels"
        required: false

jobs:
  example:
    name: ARSC Label Example
    runs-on: ubuntu-latest
    permissions:
      issues: write
      pull-requests: write
    steps:
      - name: Manage Labels
        uses: wagner-cotta/arsc-label@v1.0
        with:
          token: ${{secrets.PAT}}
          operation: ${{ github.event.inputs.operation }}
          labels: ${{ github.event.inputs.labels }}
          object-id: ${{ github.event.inputs.obj-id }}
```

##### Note:
- This action was created for personal use, but feel free to use it in your projects as well. 
  Any issues, suggestions, or questions, please feel free to reach out.


### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.