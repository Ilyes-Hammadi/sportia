import json

from jinja2 import Template


def init_google_json():
    json = """{
  "web": {
    "client_id": "{{client_id}}",
    "project_id": "{{project_id}}",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "{{client_secret}}",
    "javascript_origins": [
      "http://localhost:5000"
    ],
    "redirect_uris": ""
  }
}"""
    file = open('google_client_secrets.json', 'w')
    file.write(json)
    file.close()


def init_facebook_json():
    json = """{
  "web": {
    "app_id": "{{app_id}}",
    "app_secret": "{{app_secret}}"
  }
}"""
    file = open('fb_client_secrets.json', 'w')
    file.write(json)
    file.close()


def google_setup(client_id, client_secret, project_id):
    init_google_json()

    cs_json = open('google_client_secrets.json').read()

    cs_json = Template(cs_json).render(client_id=client_id, project_id=project_id, client_secret=client_secret)

    open('google_client_secrets.json', 'w').write(cs_json)


def facebook_setup(app_id, app_secret):
    init_facebook_json()

    cs_json = open('fb_client_secrets.json').read()

    cs_json = Template(cs_json).render(app_id=app_id, app_secret=app_secret)

    open('fb_client_secrets.json', 'w').write(cs_json)


def api_config():
    google_json = json.loads(open('google_client_secrets.json').read())
    facebook_json = json.loads(open('fb_client_secrets.json').read())

    config = {
        'google_plus': google_json,
        'facebook': facebook_json
    }

    return config


if __name__ == '__main__':
    api_config()

    choice = None
    while (choice != 99):
        print '------------------- Welcome to Sportia Api Setup ----------------------'
        print '1. Google+ Api'
        print '2. Facebook Api'
        print '99. Exit'
        choice = int(raw_input('Your Choice (ex: 1): '))

        if choice == 1:
            print '----------------------Google Plus Api ---------------------------------'
            client_id = raw_input('Enter the Client ID: ')
            project_id = raw_input('Enter the Project ID: ')
            client_secret = raw_input('Enter the Client Secret: ')

            google_setup(client_id=client_id, client_secret=client_secret, project_id=project_id)
        elif choice == 2:
            print '----------------------Facebook Api ---------------------------------'
            app_id = raw_input('Enter the App ID: ')
            app_secret = raw_input('Enter the App Secret: ')

            facebook_setup(app_id=app_id, app_secret=app_secret)
        elif choice == 99:
            print 'Bye Bye ;)'
        else:
            print 'Key Error'
