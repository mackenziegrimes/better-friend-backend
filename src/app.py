from .app_wrapper import AppWrapper

wrapper = AppWrapper()
app = wrapper.app

if __name__ == "__main__":
    app.run()
