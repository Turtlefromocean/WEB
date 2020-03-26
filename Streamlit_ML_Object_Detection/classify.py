from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array

from tensorflow.keras.applications.vgg16 import VGG16, decode_predictions, preprocess_input
from tensorflow.keras.applications.xception import Xception, decode_predictions, preprocess_input


def predict(image1, selected_model):
	model = Xception()
	image = load_img(image1, target_size=(299, 299))

	if selected_model == "vgg16":
		model = VGG16()
		image = load_img(image1, target_size=(224,224))

	image = img_to_array(image)
	image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

	image = preprocess_input(image)
	result = model.predict(image)
	label = decode_predictions(result)

	label = label[0][0]
	
	return label