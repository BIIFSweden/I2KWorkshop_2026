"""
Plumbing for the image registration workshop notebook (grayscale/RGB
conversion, size matching, pre-shifting, a checkerboard blend, a
colorblind-friendly overlay) -- not registration logic, so kept out of
the notebook itself.
"""

import itk
import numpy as np
from skimage.color import rgb2gray


def read_rgb(path):
    """Read an image file's raw RGB array (H, W, 3), float32, 0-255 scale.

    Drops the file's spacing/origin/direction on purpose -- see
    `read_grayscale` for why everything here uses plain pixel units.
    """
    return itk.GetArrayFromImage(itk.imread(path)).astype(np.float32)


def read_grayscale(path):
    """Read an RGB image file and return a single-channel itk.Image.

    Converts with `skimage.color.rgb2gray` (Rec. 709 luma), rescaled back
    to 0-255. `itk.GetImageFromArray` makes a fresh image with no
    spacing/origin/direction, so those are copied from the source --
    except spacing, which is forced to 1 (pixels): these files carry DPI
    metadata itk reads as spacing=0.1, which would make elastix report
    transforms in that unit while anything built later with
    `itk.GetImageFromArray` defaults to spacing=1, silently disagreeing.
    """
    rgb_image = itk.imread(path)
    gray_arr = (rgb2gray(itk.GetArrayFromImage(rgb_image)) * 255).astype(np.float32)
    gray_image = itk.GetImageFromArray(gray_arr)
    gray_image.CopyInformation(rgb_image)
    gray_image.SetSpacing([1.0, 1.0])
    return gray_image


def pad_to_shape(image, shape):
    """Embed an itk image at the top-left of a zero-filled canvas of the given (height, width)."""
    arr = itk.GetArrayFromImage(image)
    canvas = np.zeros(shape, dtype=arr.dtype)
    canvas[tuple(slice(0, s) for s in arr.shape)] = arr
    padded = itk.GetImageFromArray(canvas)
    padded.CopyInformation(image)  # spacing/origin/direction don't survive GetImageFromArray otherwise
    return padded


def rgb_channel_to_padded_image(rgb_arr, channel, shape, spacing=1.0):
    """Pull one channel out of an (H, W, 3) RGB array as a padded itk.Image.

    `transformix` only works on scalar images, so warping an RGB image
    means splitting it into three of these and recombining afterwards.

    `spacing` must match whatever spacing the transform you're about to
    apply was declared with (its parameter map's own `Spacing` field) --
    transformix uses it to convert the physical coordinates it computes
    back into pixel indices on this image. Get it wrong and transformix
    silently samples only a fraction of the image and stretches that over
    the full output, i.e. a "zoomed in" result. Defaults to 1 (plain
    pixels), matching `read_grayscale`; pass the resized-to-full-resolution
    transform's own declared spacing when applying one of those instead.
    """
    channel_image = itk.GetImageFromArray(np.ascontiguousarray(rgb_arr[:, :, channel]))
    channel_image.SetSpacing([spacing, spacing])
    return pad_to_shape(channel_image, shape)


def pad_to_common_size(image_a, image_b):
    """Embed two itk images into zero-filled canvases of the same shape.

    elastix can register images of different sizes, but the numpy-based
    overlays, checkerboards and NCC metrics elsewhere in the notebook
    assume the two arrays line up index-for-index.

    Note: `itk.GetArrayFromImage` returns a `[row, col]` (`[y, x]`) array
    -- the reverse of `itk.Image`'s own `(x, y)` `Size`.
    """
    arr_a = itk.GetArrayFromImage(image_a)
    arr_b = itk.GetArrayFromImage(image_b)

    if arr_a.shape == arr_b.shape:
        return image_a, image_b

    max_shape = tuple(max(a, b) for a, b in zip(arr_a.shape, arr_b.shape))
    return pad_to_shape(image_a, max_shape), pad_to_shape(image_b, max_shape)


def shift_image(image, tx, ty):
    """Pre-shift an itk image by (tx, ty) pixels, zero-filling the uncovered border (no wraparound).

    Mirrors elastix's translation convention, `output(x) = moving(x + t)`,
    so pre-shifting the moving image by a coarse search's result gives
    the fine registration stages a good starting point.
    """
    arr = itk.GetArrayFromImage(image)
    h, w = arr.shape
    out = np.zeros_like(arr)
    src_y = np.arange(h) + int(round(ty))
    src_x = np.arange(w) + int(round(tx))
    valid_y = (src_y >= 0) & (src_y < h)
    valid_x = (src_x >= 0) & (src_x < w)
    out[np.ix_(valid_y, valid_x)] = arr[np.ix_(src_y[valid_y], src_x[valid_x])]
    shifted = itk.GetImageFromArray(out)
    shifted.CopyInformation(image)
    return shifted


def checkerboard(a, b, tile=32):
    """Tile two same-shaped (H, W) or (H, W, 3) arrays into alternating blocks."""
    yy, xx = np.indices(a.shape[:2])
    mask = ((yy // tile) + (xx // tile)) % 2 == 0
    if a.ndim == 3:
        mask = mask[:, :, np.newaxis]
    return np.where(mask, a, b)


def magenta_cyan_overlay(image_a, image_b):
    """Blend two [0, 1] grayscale images so agreement reads as gray, not yellow.

    `image_a` tints magenta (R+B), `image_b` tints cyan (G+B), and their
    shared blue channel is the mean of the two -- where the images truly
    agree, R=G=B and the pixel looks neutral gray.
    """
    overlay = np.zeros((*image_a.shape, 3), dtype=np.float32)
    overlay[:, :, 0] = image_a
    overlay[:, :, 1] = image_b
    overlay[:, :, 2] = (image_a + image_b) / 2
    return overlay
