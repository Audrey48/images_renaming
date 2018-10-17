# images_renaming
Automatically rename jpg images with their capture time

## Goal
If you have a lot of images with automatic unsignificant names, it's hard to manage them.
However, usually, Jpeg images have their Date and Time of capture embedded in thei metadata.

This program can be used to automatically rename images with their capture Date and Time.

**Note** : I used this program to manage thousands of images restored from a formated HDD.

##How to use this program

### Install
To run this program, you have to install:
- Python 3
- Pillow : ``` pip install Pillow ```

### Use
- Copy your images to rename in _pictures_ directory
- Run ```python main.py```
  - Images with new names will be saved in _result_ folder
  - Original images are moved to _copied_ folder 
  - Images which can't be opened or with an undefined DateTime are moved to _issues_ folder
  - Images with conflicts are let in the _pictures_ folder (images with same DateTime but which are different)
