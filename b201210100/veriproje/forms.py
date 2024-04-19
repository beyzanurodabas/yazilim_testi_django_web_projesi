from django import forms

class GitHubRepoForm(forms.Form):
    repo_url = forms.URLField(label='Repository URL', max_length=200)