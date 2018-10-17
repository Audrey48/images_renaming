import os
from fnmatch import fnmatch 
import shutil
import filecmp

from PIL import Image
from PIL.ExifTags import TAGS
 
 
class JpegImage:
    def __init__(self, filename=None, exif=None):
        self.filename = filename
        self.exif = exif
        self.time = None
 
    def get_exif(self):
        ret = {}
        try:
            i = Image.open(self.filename)
        except:
            print('Skipping unreadable image' + self.filename)
            return
        self.exif = i._getexif()
        #print('info: {}'.format(self.exif))
        return self.exif

    def get_field(self,field) :
        if self.exif == None :
            self.get_exif()
      
        if self.exif == None :
            print("Cannot extract exif from " + self.filename)
            return False

        for (tag_id,field_value) in self.exif.items():
            #print("Tag : " + str(TAGS.get(tag_id)) + " ; value : " + str(field_value))
            if TAGS.get(tag_id) == field :
                self.time = field_value
        
        if self.time == None :
            print("No time attribute for " + self.filename)
            return False
        
        return True

 
if __name__ == '__main__':
    input_path = ".\\pictures"
    output_path = ".\\result"
    copied_path = ".\\copied"
    issues_path = ".\\issues"
    pattern = "*.jpeg"
    my_img_dictionary = dict()
    input_issues = 0
    duplicated_files = 0
    input_conflicts = 0
    output_conflicts = 0

    
    if not os.path.exists(issues_path):
        os.makedirs(issues_path)

    #parse all images
    for element in os.listdir(input_path):
        if fnmatch(element, pattern):
            issue_encountered = False
            img_name = input_path + '\\' + element
            print(img_name)
            myImage = JpegImage(filename=img_name)
            ret = myImage.get_field('DateTime')

            if not ret:
                print("Error while extracting data from " + img_name)
                shutil.move(img_name, img_name.replace(input_path, issues_path))
                issue_encountered = True

            if not issue_encountered :
                if myImage.time in my_img_dictionary:
                    my_img_dictionary[myImage.time].append(img_name)
                else:
                    my_img_dictionary[myImage.time] = [img_name]

    #rename and move images
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    if not os.path.exists(copied_path):
        os.makedirs(copied_path)

    for x, y in my_img_dictionary.items():
        conflict = False
        print(x, y)

        time_name = x.replace(":", "-")
        time_name = time_name.replace(" ", "_")
        time_name = time_name + ".JPG"
        print(time_name)

        if not os.path.exists(".\\result\\"+time_name):
            #print("save renamed image in output directory")
            shutil.copy2(y[0], ".\\result\\"+time_name)
        else:
            if not filecmp.cmp(y[0], ".\\result\\"+time_name, shallow=False) :
                print("File already exists in output directory but differs")
                output_conflicts += 1
                conflict = True

        if not conflict:
            #print("move original image")
            if not os.path.exists(y[0].replace(input_path, copied_path)):
                shutil.move(y[0], y[0].replace(input_path, copied_path))
            else:
                if filecmp.cmp(y[0], y[0].replace(input_path, copied_path)):
                    #print("file already exists in copied directory but is the same")
                    shutil.move(y[0], y[0].replace(input_path, copied_path))
           
            if len(y) != 1 :
                print("Too many images for key " + x)
                for i in range (1, len(y)):
                    print(y[0] + " and " + y[i])
                    compare = filecmp.cmp(y[0].replace(input_path, copied_path), y[i], shallow=False)
                    if compare == True :
                        print("Files are the same")
                        duplicated_files += 1
                        shutil.move(y[i], y[i].replace(input_path, copied_path))

                    else:
                        print("Files differ")
                        input_conflicts += 1

    print("duplicated files : " + str(duplicated_files))
    print("input_conflicts : " + str(input_conflicts))
    print("output_conflicts : " + str(output_conflicts))

    