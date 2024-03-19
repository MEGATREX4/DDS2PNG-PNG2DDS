# DDS2PNG-PNG2DDS
This Flask web application allows users to upload images and convert them between PNG and DDS formats. It automatically converts images placed in the `input` folder and saves the converted images in the `converted` folder.

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies using pip:
   ```pip install -r requirements.txt```

## Usage
1. Run the Flask application: ```python app.py```
2. Open your web browser and go to http://localhost:5000/.
3. You'll see a dropdown menu to select the conversion type (PNG to DDS or DDS to PNG).
4. Select the desired conversion type and click the "Convert Files" button.
5. The application will automatically convert the images in the input folder and save the converted images in the converted folder.

## Configuration
You can configure the following parameters in the app.py file:

* UPLOAD_FOLDER: Path to the folder where uploaded images are stored.
* CONVERTED_FOLDER: Path to the folder where converted images will be saved.
* ALLOWED_EXTENSIONS: Set of allowed file extensions for image files.
