import urlparse

from django import forms


class SmartURLField(forms.URLField):
    def clean(self, value):
        value = unicode.strip(value)
        return super(SmartURLField, self).clean(value)


class RepoForm(forms.Form):
    repo_url = SmartURLField(label='Enter a Github repostitory URL',
            widget=forms.TextInput(attrs={'size':'80'}),
            max_length=512, verify_exists=True,
            error_messages={'required':
                        'Please enter a valid Github Repository URL'})

    def clean_repo_url(self):
        url = self.cleaned_data['repo_url']
        if not url.startswith('https://github.com/'):
            raise forms.ValidationError('Please make sure the URL starts '
                    'with https://github.com/')

        parts = urlparse.urlsplit(url)
        path_segments = filter(None, parts[2].split('/'))
        if len(path_segments) != 2:
            raise forms.ValidationError('Please make sure the URL '
                    'is a valid respository.')
        return url
