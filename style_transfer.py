import functools
import os
from matplotlib import gridspec, pyplot
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import cv2
# %%
def crop_center(image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape)
    return image

@functools.lru_cache(maxsize=None)
def load_image(image_path, image_size=(256, 256), preserve_aspect_ratio=True):
    """Loads and preprocesses images."""
    # Cache image file locally.
    # image_path = tf.keras.utils.get_file(os.path.basename(image_url)[-128:], image_url)
    # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
    img = plt.imread(image_path).astype(np.float32)[np.newaxis, ...]
    if img.max() > 1.0:
        img = img / 255.
    if len(img.shape) == 3:
        img = tf.stack([img, img, img], axis=-1)
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img

def save_n(images, path, titles=('',)):
    n = len(images)
    image_sizes = [image.shape[1] for image in images]
    w = (image_sizes[0] * 6) // 320
    plt.figure(figsize=(w  * n, w))
    gs = gridspec.GridSpec(1, n, width_ratios=image_sizes)
    for i in range(n):
        plt.subplot(gs[i])
        plt.imshow(images[i][0], aspect='equal')
        plt.axis('off')
        plt.title(titles[i] if len(titles) > i else '')
    #plt.show()
    plt.savefig(path)
    pyplot.clf()
    pyplot.cla()
    pyplot.close()

# %%
def load_model():
    hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
    hub_module = hub.load(hub_handle)
    return hub_module
  
def style_transfer(content_image, style_image): # return the filepath to the new prediction
    num = np.random.randint(1000)
    output_image_size = 384 #384
    content_img_size = (output_image_size, output_image_size)
    style_img_size = (256, 256)
    content_image = load_image(content_image, content_img_size)
    style_image = load_image(style_image, style_img_size)
    style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')
    model = load_model()
    outputs = model(content_image, style_image)
    stylized_image = outputs[0]
    #save_n([content_image], path="static/preds/content_img.jpg", titles=['content_image'])
    #save_n([style_image], path="static/preds/style_img.jpg", titles=['style_image'])
    #save_n([stylized_image], path="static/preds/stylized_img.jpg", titles=['Stylized image'])
    file_path = "static/preds/img_pred" + str(num) + ".jpg"
    save_n([content_image, style_image, stylized_image], path=file_path, titles=['content_image', 'style_image', 'Stylized image'])
    return file_path
# %%
#content_image = './imgs_bill/cat.jpg'
#style_image = './imgs_bill/wave.jpg'
#style_transfer(content_image, style_image)