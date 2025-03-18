# Server Side Installation Guide

This guide will help you install the necessary packages for the server side of your project.

## Prerequisites

Make sure you have Python installed on your machine. You can download and install it from the [Python official website](https://www.python.org/).

## Installation Steps

1. **Navigate to the server directory:**

    Open your terminal and navigate to the server directory of your project.

    ```
    cd path/to/your/project/server
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    Create a virtual environment to manage your dependencies.

    ```
    python -m venv venv
    ```

    Activate the virtual environment:

    - On Windows:

        ```
        .\venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```
        source venv/bin/activate
        ```

3. **Install the required packages:**

    Run the following command to install all the necessary packages listed in the `requirements.txt` file.

    ```
    pip install -r requirements.txt
    ```

4. **Run the server application:**

    After the installation is complete, you can start the server application using the following command:

    ```
    uvicorn src.main:app --reload
    ```

    This will start the development server and you can view your application at `http://127.0.0.1:8000`.

## Additional Information

- If you encounter any issues during the installation, make sure your Python and pip versions are up to date.
- You can update pip to the latest version using the following command:

    ```
    python -m pip install --upgrade pip
    ```

- For any other issues, refer to the [FastAPI documentation](https://fastapi.tiangolo.com/).

Happy coding!