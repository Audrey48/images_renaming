import os
from fnmatch import fnmatch 
import shutil

from PIL import Image
from PIL.ExifTags import TAGS
 
 
class JpegImage:
    def __init__(self, filename=None, exif=None):
        self.filename = filename
        self.exif = exif
 
    def get_exif(self):
        ret = {}
        i = Image.open(self.filename)
        self.exif = i._getexif()
        #print('info: {}'.format(self.exif))
        return self.exif

    def get_field(self,field) :
      if self.exif == None :
          self.get_exif()
          
      for (tag_id,field_value) in self.exif.items():
         if TAGS.get(tag_id) == field:
            return field_value

 
if __name__ == '__main__':
    input_path = ".\\pictures"
    output_path = ".\\result"
    pattern = "*.jpg"
    my_img_dictionary = dict()

    #parse all images
    for element in os.listdir(input_path):
        if fnmatch(element, pattern):
            img_name = input_path + '\\' + element

            myImage = JpegImage(filename=img_name)
            time = myImage.get_field('DateTime')

            if time in my_img_dictionary:
                my_img_dictionary[time].append(img_name)
            else:
                my_img_dictionary[time] = [img_name]

    #rename images
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for x, y in my_img_dictionary.items():
        print(x, y)

        if len(y) != 1 :
            print("Too many images for key " + x)

        else:
            name = x.replace(":", "-")
            name = name.replace(" ", "_")
            name = name + ".JPG"
            #print(name)
            shutil.copy2(y[0], ".\\result\\"+name)


    