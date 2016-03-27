import views

if __name__ == '__main__':
    views.app.secret_key = 'super_secret_key'
    views.app.debug = True
    views.app.run(host='0.0.0.0', port=5000)
