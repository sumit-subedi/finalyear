from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageUploadForm
from PIL import Image 

import numpy as np
import cv2, base64, re, os, subprocess


@csrf_exempt
def home(request):
	# if request.method == 'POST':
	# 	image = request.POST['image']
	# 	print('image received')
	# return render(request, 'home.html')

	

	if request.method == 'POST':
		form = ImageUploadForm(request.POST, request.FILES)
		if form.is_valid():
			img = request.FILES['photo']

			with open('./test.png', 'wb+') as f:
				for chunk in img.chunks():
					f.write(chunk)
			# im1 = Image.open(request.FILES['photo'])
			# im1.save('./test.png')
			img = cv2.imread('./test.png') # Read in the image and convert to grayscale
			#0 img = np.array(im1) # Read in the image and convert to grayscale
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			gray = 255*(gray < 100).astype(np.uint8) # To invert the text to white
			coords = cv2.findNonZero(gray) # Find all non-zero points (text)
			x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
			rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image
			# rect = cv2.rotate(rect, cv2.cv2.ROTATE_90_CLOCKWISE)
			# cv2.imshow("Cropped", rect) # Show it
			# cv2.waitKey(0)
			# cv2.destroyAllWindows()
			cv2.imwrite('./SimpleHTR-master/data/test.png', rect)

			# rect.save('./SimpleHTR-master/data/test.png')
			# im1.save('./test.png')
			os.chdir('./SimpleHTR-master/src')
			proc = subprocess.Popen(["python", "main.py"], stdout=subprocess.PIPE, shell=False)
	
			(out, err) = proc.communicate()
			print('here')
			os.chdir('../../')
			print('here')

			output = str(out)
			message = output[output.index('Recog'):].strip()
			recognized = ""
			for i in range(message.index('"')+1, 100):
				if message[i] == '"':
					break
				recognized += message[i]
			probability = message[message.index('0'):-5]
			
			img = form.save()
			ctx = {}
			ctx['recognized'] = recognized
			ctx['probability'] = probability
			with open('./SimpleHTR-master/data/test.png', "rb") as image_file:
				image_data = base64.b64encode(image_file.read()).decode('utf-8')
			ctx["image"] = image_data
			ctx["error"] = False
			return JsonResponse(ctx)

		else:
		   return JsonResponse({'error': True, 'errors': form.errors})
	else:
		form = ImageUploadForm()
		return render(request, 'home.html', {'form': form})
