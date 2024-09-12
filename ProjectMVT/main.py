from app import create_app

app = create_app(config_type='dev')

if __name__ == '__main__':
    app.run()