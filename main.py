import os
from fnmatch import fnmatch 
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
    path = ".\\pictures"
    pattern = "*.jpg"
    my_img_dictionary = dict()
    
    for element in os.listdir(path):
        if fnmatch(element, pattern):
            img_name = path + '\\' + element

            myImage = JpegImage(filename=img_name)
            time = myImage.get_field('DateTime')

            if time in my_img_dictionary:
                my_img_dictionary[time].append(img_name)
            else:
                my_img_dictionary[time] = [img_name]

    for x, y in my_img_dictionary.items():
        print(x, y)

