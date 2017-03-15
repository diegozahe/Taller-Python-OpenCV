import cv2


def checkfile(archivo, frame):
	try:
		fichero = open(archivo)
		fichero.close()
		print("La imagen existe")

		return True

	except OSError:
		cv2.imwrite("fondo.jpg", frame)
		print("La imagen se ha creado")

		return True


# Cargamos el vídeo
camara = cv2.VideoCapture(1)
fondo = None
archivoLeido = False

while True:
	# Leemos el siguiente frame
	(grabbed, frame) = camara.read()

	# Miramos si tenemos el fondo establecido, si no es asi lo establecemos
	if not archivoLeido:
		# Creamos la imagen fondo
		archivoLeido = checkfile("fondo.jpg", frame)
		fondo = cv2.cvtColor(cv2.imread("fondo.jpg"), cv2.COLOR_BGR2GRAY)

	# Convertimos a escala de grises
	gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Calculo de la diferencia entre el fondo y el frame actual
	resta = cv2.absdiff(fondo, gris)

	# Aplicamos un umbral
	umbral = cv2.threshold(resta, 50, 255, cv2.THRESH_BINARY)[1]

	# Hacemos una copia de umbral
	umbralCopy = umbral.copy()

	# Buscamos contorno en la imagen
	im, contornos, hierarchy = cv2.findContours(umbralCopy, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

	contPersonas = 0
	for c in contornos:
		# Eliminamos los contornos más pequeño
		contorno = cv2.contourArea(c)

		# Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
		(x1, y1, w, h) = cv2.boundingRect(c)

		if contorno > 5000:
			# Dibujamos el rectángulo del bounds											
			cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), (0, 255, 0), 2)
			contPersonas += 1

	print("Hay", contPersonas, "personas")

	# Mostramos el video
	cv2.imshow("Camara", frame)
	cv2.imshow("Gris", gris)
	cv2.imshow("Umbral", cv2.pyrDown(umbral))
	cv2.imshow("Resta", cv2.pyrDown(resta))
	cv2.imshow("fondo", fondo)
	# cv2.imshow("Contorno", cv2.pyrDown(umbralCopy))

	# Capturamos una tecla para salir
	key = cv2.waitKey(1) & 0xFF

	# Si ha pulsado la letra s, salimos
	if key == ord("s"):
		break

# Cuando hemos acabado, desvinculamos la captura de video
camara.release()
cv2.destroyAllWindows()
