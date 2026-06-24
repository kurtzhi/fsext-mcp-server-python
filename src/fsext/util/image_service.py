# SPDX-FileCopyrightText: 2026 https://github.com/kurtzhi/fsext-mcp-server-python
# SPDX-License-Identifier: Apache-2.0

# Copyright 2026 https://github.com/kurtzhi/fsext-mcp-server-python
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Service for performing image-related operations, including mime detection, resize, crop and rotation.
All file path arguments are validated via unified check_utils utilities.
"""
from pathlib import Path

from PIL import Image

from .file_service import get_file_extension
from .check_utils import (
    require_non_blank,
    require_readable_file,
    require_writable_parent_directory
)


def resize(
        source_image_path: str,
        dest_image_path: str,
        keep_aspect_ratio: bool,
        pad_to_target: bool,
        target_width: int,
        target_height: int,
):
    """
    Resizes an image from the source path to the specified target dimensions, supports transparent padding.
    Auto switch canvas color mode to avoid save failure for non-alpha formats like JPG.

    :param source_image_path: The path to the source image.
    :param dest_image_path: The path to save the resized image.
    :param keep_aspect_ratio: If true, maintains the original aspect ratio with thumbnail scaling.
    :param pad_to_target: If true, fill blank space with padding to target canvas size.
    :param target_width: Target canvas pixel width, must be positive integer.
    :param target_height: Target canvas pixel height, must be positive integer.
    :raises ValueError: Path arguments blank, source unreadable file, destination parent not writable,
                        target_width/target_height <= 0
    """
    require_non_blank(source_image_path, "source_image_path")
    require_non_blank(dest_image_path, "dest_image_path")

    if target_width <= 0 or target_height <= 0:
        raise ValueError("target_width and target_height must be positive integers")

    input_file = Path(source_image_path)
    require_readable_file(input_file, "image_path")

    output_file = Path(dest_image_path)
    require_writable_parent_directory(output_file, "dest_image_path")
    output_format = get_file_extension(dest_image_path, "dest_image_path").lower()

    with Image.open(input_file) as img:
        if keep_aspect_ratio:
            img.thumbnail((target_width, target_height))
            actual_width, actual_height = img.size
        else:
            img = img.resize((target_width, target_height), Image.LANCZOS)
            actual_width, actual_height = target_width, target_height

        if pad_to_target:
            if output_format in ("jpg", "jpeg"):
                fill_color = (255, 255, 255)
                canvas_mode = "RGB"
            else:
                fill_color = (255, 255, 255, 0)
                canvas_mode = "RGBA"
            new_img = Image.new(canvas_mode, (target_width, target_height), fill_color)
            new_img.paste(
                img, ((target_width - actual_width) // 2, (target_height - actual_height) // 2)
            )
            new_img.save(output_file)
        else:
            img.save(output_file)


def crop(
        source_image_path: str,
        dest_image_path: str,
        x: int,
        y: int,
        width: int,
        height: int,
):
    """
    Crops a rectangular sub-region from an image and saves to destination path.
    Pillow crop format: (left, upper, right, lower). All size params must be >= 0.

    :param source_image_path: The path to the source image.
    :param dest_image_path: The path to save the cropped image.
    :param x: X coordinate of crop region top-left corner (pixel), >=0
    :param y: Y coordinate of crop region top-left corner (pixel), >=0
    :param width: Pixel width of crop box, must be positive
    :param height: Pixel height of crop box, must be positive
    :raises ValueError: Path arguments blank, source unreadable file, destination parent not writable,
                        negative crop coordinate/size
    """
    require_non_blank(source_image_path, "source_image_path")
    input_file = Path(source_image_path)
    require_readable_file(input_file, "image_path")

    if x < 0 or y < 0 or width <= 0 or height <= 0:
        raise ValueError("Crop x/y cannot be negative, width/height must be positive")

    require_non_blank(dest_image_path, "dest_image_path")
    output_file = Path(dest_image_path)
    require_writable_parent_directory(output_file, "dest_image_path")

    with Image.open(input_file) as img:
        # Pillow crop format: (left, upper, right, lower)
        cropped_img = img.crop((x, y, x + width, y + height))
        cropped_img.save(output_file)


def rotate_image(
        source_image_path: str,
        dest_image_path: str,
        degrees: float
):
    """
    Rotates an image by specified clockwise degrees, expand canvas to avoid content cropping.
    Pillow native rotate is counter-clockwise, negative degree converts to clockwise rotation.

    :param source_image_path: The path to the source image.
    :param dest_image_path: The path to save the rotated image.
    :param degrees: Clockwise rotation angle in floating-point degrees.
    :raises ValueError: Path arguments blank, source unreadable file, destination parent not writable
    """
    require_non_blank(source_image_path, "source_image_path")
    input_file = Path(source_image_path)
    require_readable_file(input_file, "image_path")

    require_non_blank(dest_image_path, "dest_image_path")
    output_file = Path(dest_image_path)
    require_writable_parent_directory(output_file, "dest_image_path")

    degrees = degrees % 360

    with Image.open(input_file) as source:
        # expand=True auto enlarge canvas to hold full rotated content, BICUBIC for smooth resample
        rotated_image = source.rotate(-degrees, expand=True, resample=Image.BICUBIC)
        rotated_image.save(fp=output_file)
