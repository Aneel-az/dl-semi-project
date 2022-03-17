import os
import shutil

from PIL import Image


def overwrite_folder(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)


def _get_new_size(width, height, size):
    width_ratio = size[0] / width
    height_ratio = size[1] / height

    ratio = min(width_ratio, height_ratio)
    new_size = (int(width * ratio), int(height * ratio))

    return new_size


def resize(dir_path, result_dir_path, size: tuple):
    overwrite_folder(result_dir_path)
    for image_name in os.listdir(dir_path):
        image = Image.open(f"{dir_path}/{image_name}")
        width, height = image.size
        ratio_size = _get_new_size(width, height, size)
        new_image_sized = image.resize(ratio_size)
        new_image = Image.new(new_image_sized.mode, size, (0, 0, 0))
        new_image.paste(new_image_sized, (0, 0))
        new_image.save(f'{result_dir_path}/{image_name}')


def split_data(dir_path: str, output_dir_path: str, ratio: float):
    overwrite_folder(f'data/train/{output_dir_path}')
    overwrite_folder(f'data/test/{output_dir_path}')
    filenames = os.listdir(dir_path)
    train_size = int(ratio * len(filenames))
    train_filenames = filenames[:train_size]
    test_filenames = filenames[train_size:]
    for image_name in train_filenames:
        image = Image.open(f"{dir_path}/{image_name}")
        image.save(f'data/train/{output_dir_path}/{image_name}')
    for image_name in test_filenames:
        image = Image.open(f"{dir_path}/{image_name}")
        image.save(f'data/test/{output_dir_path}/{image_name}')


def prepare_data(path: str, image_wanted_size: tuple, split_ratio: float):
    resize(f"{path}/cats", "resized/cats", image_wanted_size)
    resize(f"{path}/cat_missing", "resized/cat_missing", image_wanted_size)
    split_data("resized/cats", "cats", split_ratio)
    split_data("resized/cat_missing", "cat_missing", split_ratio)


# example
prepare_data(
    path="",
    image_wanted_size=(256, 192),
    split_ratio=0.8,
)




#

# def prepare_data(hyper_params, target_size):
#   train_data_gen = ImageDataGenerator(
#     rescale=1./255,
#     shear_range=0.2,
#     zoom_range=0.2,
#     horizontal_flip=True,
#     validation_split=hyper_params["validation_split"]
#     )
#   training_set = train_data_gen.flow_from_directory(
#     '/content/drive/MyDrive/dl1/CNN/dataset/training_set',
#     target_size=(32, 32),
#     batch_size=hyper_params["batch_size"],
#     class_mode='categorical',
#     subset='training'
#   )
#   validation_set = train_data_gen.flow_from_directory(
#   '/content/drive/MyDrive/dl1/CNN/dataset/training_set',
#     target_size=(32, 32),
#     batch_size=hyper_params["batch_size"],
#     class_mode='categorical',
#     subset='validation'
#   )

#   test_data_gen = ImageDataGenerator(rescale = 1./255)
#   test_set = test_data_gen.flow_from_directory(
#     '/content/drive/MyDrive/dl1/CNN/dataset/test_set',
#     target_size=(32, 32),
#     batch_size=hyper_params["batch_size"],
#     class_mode='categorical'
#   )
#   return {
#       "train_set": training_set,
#       "validation_set": validation_set,
#       "test_set": test_set
#   }

