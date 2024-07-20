import pickle

class AppStyle():
    with open('stylesettings', 'rb') as pickle_file:
        style = pickle.load(pickle_file)
    
    def setStyle(self, style_name):
        self.style = style_name
        with open('stylesettings', 'wb') as pickle_file:
                pickle.dump(self.style, pickle_file)