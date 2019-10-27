# Github-project-reporting

Using the github v4 API create a quick report of what a project board has.

This is a slightly modified version of a script I created to make reports elsewhere. So
it might not have the best defaults. But if you like the example output you can easily
generate one for yourself using any project board you have access to.

## Requirements

Single pip dependency `requests`

`pip install request`

[Github access token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/), which you should place in a file called `github-oaut` inside the same directory as script `create_project_report.p`.

## Usage

Once you have the dependencies and your access token in the file, you can create a markdown report using as such:

```sh
python create_project_report.py -u YOUR_USERNAME -r YOUR_PROJECTS_REPO
```

## Limits

Only works on project boards made for a repo and not a user. Only searches and handles the first
project board it can find for a repository.
