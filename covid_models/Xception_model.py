# Build Xception model

from tensorflow.keras.models import Model
from tensorflow.keras import layers
from tensorflow.keras.applications import Xception

class XceptionNet():
    def __init__(self, weights):
        self.weights = weights
        
    def buildBaseModel(self, img_size):
        base_model = Xception(weights='imagenet', include_top=False, 
                                 input_shape = (img_size,img_size,3))
        x = base_model.output
        x = layers.GlobalAveragePooling2D()(x)
        predictions = layers.Dense(1, activation='sigmoid', name='last')(x)
        model = Model(inputs=base_model.input, outputs=predictions)
        model.load_weights(self.weights)
        return model
    
    def freeze(self, model):
        for layer in model.layers[:133]:
            layer.trainable = False
        for layer in model.layers[133:]:
            layer.trainable = True
            
        return model
    
    def buildTunerModel(self, img_size):
        base_model = Xception(weights='imagenet', include_top=False, 
                                 input_shape = (img_size,img_size,3))
        base_model.load_weights(self.weights, by_name = True)
        return base_model
    
    def buildDropModel(self, img_size, dropout):
        base_model = Xception(weights=None, include_top=False, 
                                 input_shape = (img_size,img_size,3))
        x = base_model.output
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dropout(dropout)(x)
        predictions = layers.Dense(1, activation='sigmoid', name='last')(x)
        model = Model(inputs=base_model.input, outputs=predictions)
        model.load_weights(self.weights)
        return model
