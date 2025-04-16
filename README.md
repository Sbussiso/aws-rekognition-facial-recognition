# Face Recognition Application

This application uses Amazon Rekognition to perform real-time face recognition using a webcam. It allows you to index a known face image and then detect and recognize that face in the webcam feed.

## Introduction

The Face Recognition Application is a Python-based project that leverages the power of Amazon Rekognition, a computer vision service provided by Amazon Web Services (AWS). It enables real-time face recognition by capturing video from a webcam, detecting faces in each frame, and comparing them against a pre-indexed known face.

The application is designed to be configurable and extensible, allowing you to customize various settings such as the AWS region, similarity threshold, and known face image. It also includes logging functionality to track the application's progress and any errors that may occur.

## Features

- Real-time face recognition using a webcam
- Indexing a known face image into an Amazon Rekognition collection
- Configurable similarity threshold for face matching
- Logging to both console and file
- Environment variable support for AWS credentials and region

## Prerequisites

Before running the Face Recognition Application, ensure you have the following prerequisites installed:

- Python 3.6 or later
- OpenCV (cv2) library for video capture and display
- AWS SDK for Python (Boto3) library
- python-dotenv library for loading environment variables

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/face-recognition-app.git
```

2. Navigate to the project directory:

```bash
cd face-recognition-app
```

3. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
```

4. Activate the virtual environment:

   - On Windows:
   ```bash
   venv\Scripts\activate
   ```

   - On Unix or macOS:
   ```bash
   source venv/bin/activate
   ```

5. Install the required Python packages:

```bash
pip install -r requirements.txt
```

6. Set up your AWS credentials:

   - Create a new file named `.env` in the project root directory.
   - Add the following lines to the `.env` file, replacing `<your_access_key_id>` and `<your_secret_access_key>` with your actual AWS credentials:

   ```
   AWS_ACCESS_KEY_ID=<your_access_key_id>
   AWS_SECRET_ACCESS_KEY=<your_secret_access_key>
   ```

   - Optionally, you can also set the `AWS_REGION` environment variable in the `.env` file if you want to use a region other than the default `us-east-1`.

7. Prepare your known face image:

   - Place your known face image in the project root directory with the filename `me.jpg`.

## Usage

1. Run the application:

```bash
python main.py
```

2. The application will initialize the Rekognition client, create or verify the existence of the face collection, and index your known face image.

3. Once the indexing is complete, the webcam feed will open, and the application will start performing real-time face recognition.

4. If a face match is found above the configured similarity threshold, a green text overlay with the matched face ID will be displayed on the video feed.

5. Press the 'q' key to exit the application.

6. The application logs will be written to both the console and a file named `rekognition_app.log` in the project root directory.

## Contributing

Contributions to the Face Recognition Application are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the project's GitHub repository.

When contributing, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes and ensure that the code follows the project's coding style and conventions.
3. Write appropriate tests for your changes, if applicable.
4. Update the documentation (README.md) if necessary.
5. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- The Face Recognition Application was developed using the [Amazon Rekognition](https://aws.amazon.com/rekognition/) service and the [AWS SDK for Python (Boto3)](https://aws.amazon.com/sdk-for-python/).
- The OpenCV library was used for video capture and display.
- The