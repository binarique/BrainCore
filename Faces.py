import base64
import cv2
import numpy as np
import face_recognition
import io
import os


class Faces:
    def __init__(self) -> None:
        pass

    def getArrayBinary(self, encoding):
        out = io.BytesIO()
        np.save(out, encoding)
        out.seek(0)
        return out.read()

    def getNPArray(self, text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

    def getBase64Template(self, imageEncode):
        bytes = self.getArrayBinary(imageEncode)
        message_bytes = base64.b64encode(bytes).decode("utf-8")
        return message_bytes

    def getImageEncodeFromTemp(self, base64FaceEncodingString):
        deconcodeSttring = base64.b64decode(base64FaceEncodingString)
        encodefromstring = self.getNPArray(deconcodeSttring)
        return encodefromstring

    def getFaceEncodingsFromBase64Template(self, base64FaceEncodingString):
        deconcodeSttring = base64.b64decode(base64FaceEncodingString)
        encodefromstring = self.getNPArray(deconcodeSttring)
        return encodefromstring

    def getBase64FaceEncodingTemplates(self, imgpath):
        templates = []
        try:
            faceEncodings = self.getFaceEncodings(imgpath)
            for faceEncoding in faceEncodings:
                template = self.getBase64Template(faceEncoding)
                templates.append(template)
        except:
            pass
        return templates

    def getFaceEncoding(self, imgpath, index=0):
        img = cv2.imread(imgpath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        return encodes[index]

    def getFaceEncodings(self, imgpath):
        img = cv2.imread(imgpath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        return encodes

    def getFaceEncodingsFromImage(self, output):
        img = cv2.imread(output)
        Image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        Image = cv2.resize(Image, (0, 0), None, 1, 1)
        imgS = cv2.resize(Image, (0, 0), None, 0.8, 0.8)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodingCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        return encodingCurFrame

    def getTemplateFromImage(self, output):
        img = cv2.imread(output)
        Image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        Image = cv2.resize(Image, (0, 0), None, 1, 1)
        imgS = cv2.resize(Image, (0, 0), None, 0.25, 0.25)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodingCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)[0]
        base64Template = self.getBase64Template(encodingCurFrame)
        return base64Template

    def getPercentageMatch(self, templateEncoding, candidateEncodings):
        faceDist = face_recognition.face_distance(
            [templateEncoding], candidateEncodings  # known_encodings, unknown_encoding)
        )
        percentage_match = round(faceDist[0] * 100, 0)
        return percentage_match

    def MatchOne(self, templateEncoding, candidateEncodings):
        distances = face_recognition.face_distance(
            [templateEncoding], candidateEncodings  # known_encodings, unknown_encoding)
        )
        if not distances:
            return [0]  # Handle empty distance list
        min_distance = min(distances)
        max_distance = max(distances)
        epsilon = 1e-8  # Small value to prevent division by zero
        normalized_distances = [
            (d - min_distance) / (max_distance - min_distance + epsilon)
            for d in distances
        ]
        return round((1 - normalized_distances[0]) * 100, 2)

    def MatchAll(self, templateEncoding: list, candidateEncodings):
        distances = face_recognition.face_distance(
            templateEncoding, candidateEncodings  # known_encodings, unknown_encoding)
        )
        min_distance = min(distances)
        max_distance = max(distances)
        epsilon = 1e-8  # Small value to prevent division by zero
        normalized_distances = [
            (d - min_distance) / (max_distance - min_distance + epsilon)
            for d in distances
        ]
        percentage_matches = [round((1 - nd) * 100, 2) for nd in normalized_distances]
        return percentage_matches

    def compareFaces(self, templateEncoding, candidateEncodings, minimum_threshold=40):
        percentage_match = self.getPercentageMatch(templateEncoding, candidateEncodings)
        if percentage_match <= minimum_threshold:
            return True
        else:
            return False

    def detect_and_save_faces(image_path, output_folder, imageID="face"):
        # Load the image
        image = face_recognition.load_image_file(image_path)

        # Find all the faces in the image
        face_locations = face_recognition.face_locations(image)
        originalImage = cv2.imread(image_path)
        # Save each face as a separate image
        for i, face_location in enumerate(face_locations):
            top, right, bottom, left = face_location
            # Calculate width and height
            face_image = originalImage[top:bottom, left:right]
            height, width, channels = face_image.shape
            cv2.imwrite(f"{output_folder}/imageID_{i}.jpg", face_image)

    def MostAccurateMatches(
        self, KnownFaceEncodings: list, UnknownFaceEncoding, threshold=0.6
    ):
        matches = []
        face_distances = face_recognition.face_distance(
            KnownFaceEncodings,
            UnknownFaceEncoding,  # known_encodings, unknown_encoding)
        )
        for i, distance in enumerate(face_distances):
            if distance < threshold:
                matches.append((i, distance))
        matches.sort(key=lambda x: x[1])
        return matches

    def BestMatch(self, KnownFaceEncodings: list, UnknownFaceEncoding, threshold=0.6):
        matches = []
        face_distances = face_recognition.face_distance(
            KnownFaceEncodings,
            UnknownFaceEncoding,  # known_encodings, unknown_encoding)
        )
        for i, distance in enumerate(face_distances):
            if distance < threshold:
                matches.append((i, distance))
        if matches:
            matches.sort(key=lambda x: x[1])
            return matches[0]  # Return the best match
        return None  # No match found
