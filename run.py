from app import create_app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    # Run the app
    app.run(debug=True, port=8000, host="0.0.0.0")