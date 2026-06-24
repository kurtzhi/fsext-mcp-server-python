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
File read & write MCP tool module
Supports full/slice text reading, chunked binary reading, text/binary file writing.
All file access paths are limited to the permitted workspace scope.
"""
import base64

from .._instance import mcp
from ..path_restrict import restrict_workspace
from ..response_helper import response_helper
from ..util import (file_read_service, file_write_service)


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["file_path"])
async def fs_read_full_text(
        file_path: str,
        charset: str = "utf-8"
) -> dict:
    """Read full text file."""
    res = file_read_service.read_text_file(file_path, charset)
    return {"n_lines": res.n_lines, "content": res.content}


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["file_path"])
async def fs_read_text_range(
        file_path: str,
        lines_to_skip: int = 0,
        max_lines_to_read: int = 0,
        line_separator: str = "\n",
        charset: str = "utf-8"
) -> dict:
    """Read sliced text segment, -1 unlimited."""
    res = file_read_service.read_text_file_range(file_path, lines_to_skip, max_lines_to_read, line_separator, charset)
    return {"n_lines": res.n_lines, "content": res.content}


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["file_path"])
async def fs_read_binary_chunk(
        file_path: str,
        bytes_to_skip: int = 0,
        max_bytes_to_read: int = 0
) -> dict:
    """Partial binary read, base64 output, -1 unlimited."""
    res = file_read_service.read_binary_file(file_path, None, bytes_to_skip, max_bytes_to_read)
    b64 = base64.b64encode(res.bytes).decode("utf-8")
    return {"actual_length": res.actual_length, "end_of_stream": res.end_of_stream, "data_base64": b64}


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["file_path"])
async def fs_write_text(
        file_path: str,
        text: str,
        append: bool = False
) -> dict:
    """Write text file, append or overwrite."""
    file_write_service.write_text_file(file_path, text, append)
    return {"success": True}


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["file_path"])
async def fs_write_binary(
        file_path: str,
        data: bytes,
        offset: int = 0,
        length: int = -1,
        append: bool = False
) -> dict:
    """Write sliced binary bytes, -1 length uses full remaining buffer."""
    file_write_service.write_binary_file(file_path, data, offset, length, append)
    return {"success": True}
