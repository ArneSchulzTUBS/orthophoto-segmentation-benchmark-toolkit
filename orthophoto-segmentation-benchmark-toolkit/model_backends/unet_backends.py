from tensorflow.keras import optimizers
from segmentation_models import Unet

from .model_backend import ModelBackend


class UnetBackend(ModelBackend):

    def __init__(self, backbone):
        super().__init__()
        if backbone not in self.available_backbones:
            print("Backbone not found")
            raise ValueError
        self.backbone = backbone

    def compile(self):
        model_backend = Unet(self.backbone, input_shape=(self.chip_size, self.chip_size, 3), classes=6)
        model_backend.compile(
            optimizer=optimizers.Adam(lr=1e-4),
            loss='categorical_crossentropy',
            metrics=self.metrics
        )
        return model_backend