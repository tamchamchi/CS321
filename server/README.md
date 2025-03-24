# Server Side Installation Guide

This guide will help you install the necessary packages for the server side of your project.

## Prerequisites

Make sure you have Python installed on your machine. You can download and install it from the [Python official website](https://www.python.org/).

## Installation Steps

1. **Navigate to the server directory:**

   Open your terminal and navigate to the server directory of your project.

   ```sh
   cd path/to/your/project/server
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   Create a virtual environment to manage your dependencies.

   ```sh
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:

     ```sh
     .\venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```sh
     source venv/bin/activate
     ```

3. **Install the required packages:**

   Run the following command to install all the necessary packages listed in the `requirements.txt` file.

   ```sh
   pip install -r requirements.txt
   ```

4. **Run the server application:**

   After the installation is complete, you can start the server application using the following command:

   ```sh
   uvicorn src.main:app --reload
   ```

   This will start the development server and you can view your application at `http://127.0.0.1:8000`.

## Training the Model

To train the model, follow these steps:

1. **Navigate to the server directory:**

   ```sh
   cd path/to/your/project/server
   ```

2. **Activate the virtual environment:**

   - On Windows:

     ```sh
     .\venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```sh
     source venv/bin/activate
     ```

3. **Run the training script:**

   ```sh
   python .\src\models\train_model.py
   ```
   or
   ```sh
   python -m src.model.train_model
   ```

   This will train the model using the data and configurations specified in the script.

## Making the Dataset

To prepare the dataset, follow these steps:

1. **Navigate to the server directory:**

   ```sh
   cd path/to/your/project/server
   ```

2. **Activate the virtual environment:**

   - On Windows:

     ```sh
     .\venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```sh
     source venv/bin/activate
     ```

3. **Run the dataset preparation script:**

   ```sh
   python .\src\data\make_dataset.py
   ```
   or
   ```sh
   python -m src.data.make.dataset
   ```

   This will prepare the dataset and save it in the specified directory.

## Additional Information

- If you encounter any issues during the installation, make sure your Python and pip versions are up to date.
- You can update pip to the latest version using the following command:

  ```sh
  python -m pip install --upgrade pip
  ```

- For any other issues, refer to the [FastAPI documentation](https://fastapi.tiangolo.com/).

Happy coding!
