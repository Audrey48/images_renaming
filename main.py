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
        print('info: {}'.format(self.exif))
        return self.exif

    def get_field(self,field) :
      if self.exif == None :
          self.get_exif()
          
      for (tag_id,field_value) in self.exif.items():
         if TAGS.get(tag_id) == field:
            return field_value

 
if __name__ == '__main__':
    
    myImage = JpegImage(filename='.\\pictures\\DSCF9476.JPG')
    time = myImage.get_field('DateTime')
    print(time)
