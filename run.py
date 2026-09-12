from app import create_app

runner = create_app()


if __name__ == "__main__":
    runner.run(debug=True)
