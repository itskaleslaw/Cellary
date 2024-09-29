Cellary is a Flask-based web application that uses image detection to identify groceries in an image. It can help users keep track of their groceries and shows the ingredients that are available in the user's inventory when viewing a recipe.

The application uses a pre-trained model and Roboflow Influence to detect groceries in an image using an API call. The detected groceries are then displayed to the user, along with the quantity of each item, and added to the user's inventory. The user also has the option to manually add items to the inventory.

https://devpost.com/software/cellary

![{7472B9FD-4658-46EC-8365-814DF6B75473}](https://github.com/user-attachments/assets/22b496e0-7dcb-4908-a30c-c4f3409e71e4)
![{6E1A9DEB-5BE3-4BBD-96AD-D776B354278D}](https://github.com/user-attachments/assets/712abb07-602b-4057-87dc-936459ea2415)
![{6EB3DEAD-8FD3-4ECE-9F72-30A23B550160}](https://github.com/user-attachments/assets/1030b1d0-cad8-4229-949f-e1d923cf3f57)

How to run:
Install Python, Pip, and Flask. Clone the repo and run
```
python app.py
```
if on Windows and
```
python3 app.py
```
if on Mac.
