if __name__ == '__main__':
    from snow import app

    app.create_app().run('0.0.0.0', 5000)
