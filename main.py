import boto3
import logging
import cv2
import io
import sys # Import sys for exit
import os # Import os to access environment variables
from dotenv import load_dotenv # Import dotenv to load .env file

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("rekognition_app.log"),
                        logging.StreamHandler()
                    ])


# --- Constants and Configuration ---
COLLECTION_ID = 'my-face-collection'
KNOWN_FACE_IMAGE = 'me.jpg'
KNOWN_FACE_ID = "S_Bussiso_Dube"
SIMILARITY_THRESHOLD = 85.0  # Minimum similarity score to consider a match
REGION_NAME = os.getenv('AWS_REGION', 'us-east-1') # Also make region configurable via env


def initialize_rekognition():
    """Initializes and returns the AWS Rekognition client."""
    # Retrieve credentials from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    if not aws_access_key_id or not aws_secret_access_key:
        logging.error("AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) not found in environment variables or .env file.")
        sys.exit(1)

    try:
        rek = boto3.client('rekognition',
                           aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key,
                           region_name=REGION_NAME)
        logging.info(f"Successfully initialized Rekognition client in region '{REGION_NAME}'.")
        return rek
    except Exception as e:
        logging.error(f"Error initializing Rekognition client: {e}")
        sys.exit(1) # Use sys.exit

def setup_collection(rek_client, collection_id):
    """Creates or verifies the existence of the Rekognition collection."""
    try:
        response = rek_client.create_collection(CollectionId=collection_id)
        logging.info(f"Successfully created collection '{collection_id}'. ARN: {response['CollectionArn']}")
    except rek_client.exceptions.ResourceAlreadyExistsException:
        logging.info(f"Collection '{collection_id}' already exists. Proceeding.")
    except Exception as e:
        logging.error(f"Error creating or verifying collection '{collection_id}': {e}")
        sys.exit(1)

def index_known_face(rek_client, collection_id, image_path, external_id):
    """Indexes the known face image into the Rekognition collection."""
    try:
        with open(image_path, 'rb') as img:
            image_bytes = img.read()

        index_response = rek_client.index_faces(CollectionId=collection_id,
                                             Image={'Bytes': image_bytes},
                                             ExternalImageId=external_id,
                                             DetectionAttributes=['DEFAULT'])
        logging.info(f"Successfully indexed face from '{image_path}' with ID '{external_id}'.")
        # Optional: Log details about the indexed faces
        # for face_record in index_response.get('FaceRecords', []):
        #     logging.debug(f"Indexed Face ID: {face_record['Face']['FaceId']}, External ID: {face_record['Face']['ExternalImageId']}")

    except FileNotFoundError:
        logging.error(f"Error: Image file '{image_path}' not found.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error indexing face from '{image_path}': {e}")
        # Consider sys.exit(1) here too if indexing is critical

def run_face_recognition(rek_client, collection_id, similarity_threshold):
    """Starts webcam capture and performs real-time face recognition."""
    logging.info("Starting webcam capture for face recognition...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Error: Could not open webcam.")
        sys.exit(1)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                logging.warning("Failed to grab frame from webcam. Ending loop.")
                break

            ret, buf = cv2.imencode('.jpg', frame)
            if not ret:
                logging.warning("Failed to encode frame as JPEG.")
                continue
            image_bytes_frame = buf.tobytes()

            try:
                resp = rek_client.search_faces_by_image(
                    CollectionId=collection_id,
                    Image={'Bytes': image_bytes_frame},
                    FaceMatchThreshold=similarity_threshold,
                    MaxFaces=1
                )

                matches = resp.get('FaceMatches', [])
                if matches:
                    match = matches[0]
                    sim = match['Similarity']
                    face_id = match['Face']['ExternalImageId']
                    logging.info(f"Match found: External ID='{face_id}', Similarity={sim:.2f}%")

                    if sim >= similarity_threshold:
                        display_text = f"Match: {face_id}"
                        cv2.putText(frame, display_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        # Optional: Display if match found but below threshold
                        logging.debug(f"Match found below threshold: {face_id} ({sim:.2f}%)")
                        cv2.putText(frame, "Low Match", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2) # Orange text
                else:
                    logging.debug("No matching faces found in the current frame.")
                    cv2.putText(frame, "No Match", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            except Exception as e:
                logging.error(f"Error during face search: {e}")
                cv2.putText(frame, "Search Error", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                logging.info("'q' pressed. Exiting loop.")
                break
    finally:
        # --- Cleanup ---
        logging.info("Releasing webcam and destroying all OpenCV windows.")
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        logging.info("Webcam resources released.")


def main():
    """Main function to orchestrate the face recognition application."""
    rek_client = initialize_rekognition()
    setup_collection(rek_client, COLLECTION_ID)
    index_known_face(rek_client, COLLECTION_ID, KNOWN_FACE_IMAGE, KNOWN_FACE_ID)
    run_face_recognition(rek_client, COLLECTION_ID, SIMILARITY_THRESHOLD)
    logging.info("Application finished.")

if __name__ == "__main__":
    main()


