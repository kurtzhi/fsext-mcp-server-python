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
Image processing & OCR MCP tool module
Provides image resizing, cropping, rotation and Tesseract text extraction tools.
All file path parameters are restricted within the allowed workspace directory.
"""
from .._instance import mcp
from ..path_restrict import restrict_workspace
from ..response_helper import response_helper
from ..util import (image_service, ocr_service)


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["source_image_path", "dest_image_path"])
async def fs_image_resize(
        source_image_path: str,
        dest_image_path: str,
        keep_aspect_ratio: bool,
        pad_to_target: bool,
        target_width: int,
        target_height: int
) -> dict:
    """Resize image with ratio lock and padding support."""
    image_service.resize(source_image_path, dest_image_path, keep_aspect_ratio, pad_to_target, target_width,
                         target_height)
    return {"success": True}


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["source_image_path", "dest_image_path"])
async def fs_image_crop(
        source_image_path: str,
        dest_image_path: str,
        x: int,
        y: int,
        width: int,
        height: int
) -> dict:
    """Crop rectangular region from image."""
    image_service.crop(source_image_path, dest_image_path, x, y, width, height)
    return {"success": True}


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["source_image_path", "dest_image_path"])
async def fs_image_rotate(
        source_image_path: str,
        dest_image_path: str,
        degrees: float
) -> dict:
    """Rotate image clockwise, expand canvas to retain full content."""
    image_service.rotate_image(source_image_path, dest_image_path, degrees)
    return {"success": True}


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["image_path"])
async def fs_ocr_extract_text(
        image_path: str,
        tesseract_cmd_path: str,
        lang: str,
        tessdata_path: str = ""
) -> dict:
    """Extract text from image via Tesseract OCR."""
    text = ocr_service.extract_text(image_path, tesseract_cmd_path, lang, tessdata_path)
    return {"ocr_text": text}
