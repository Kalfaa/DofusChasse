import cv2 as cv
class CvUtil:

    @staticmethod
    def print_result_matching(image,top_left,bottom_right):
        cv.rectangle(image, top_left, bottom_right,
                     color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
        cv.imwrite('test.jpg', image)

    @staticmethod
    def save_image(name,image):
        cv.imwrite(name, image)

    @staticmethod
    def extract_rectangle_from_image(image,y,x,l,h):
        return image[x:x+l,y:y+h]
