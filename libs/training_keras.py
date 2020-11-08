from tensorflow.keras import optimizers, metrics
from libs import datasets_keras
from libs.config import LABELMAP
from libs.custom_metrics import MyMeanIOU
import numpy as np

import wandb
from wandb.keras import WandbCallback

def train_model(dataset, model):
    epochs = 15
#     epochs = 0
    lr     = 1e-4
    size   = 300
    wd     = 1e-2
    bs     = 4 # reduce this if you are running out of GPU memory
    pretrained = True

    config = {
        'epochs' : epochs,
        'lr' : lr,
        'size' : size,
        'wd' : wd,
        'bs' : bs,
        'pretrained' : pretrained,
    }

    wandb.config.update(config)

    model.compile(
        optimizer=optimizers.Adam(lr=lr),
        loss='categorical_crossentropy',
        metrics=[
            metrics.Precision(top_k=1, name='precision'),
            metrics.Recall(top_k=1, name='recall'),
            MyMeanIOU(num_classes=6, name='mIOU'),
        ]
    )

    train_data, valid_data = datasets_keras.load_dataset(dataset, bs)
    _, ex_data = datasets_keras.load_dataset(dataset, 10)
    model.fit(
        train_data,
        validation_data=valid_data,
        epochs=epochs,
        callbacks=[
            WandbCallback(
            )
        ]
    )
