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
File operation tool collection for fsext-mcp-server
Provides all basic single-file manipulation MCP tools, with workspace path access control.
Covers file creation, deletion, metadata query, existence check, copy and move operations.
All tools enforce workspace directory restriction to prevent unauthorized path access.
"""
from .._instance import mcp
from ..path_restrict import restrict_workspace
from ..response_helper import response_helper
from ..util import (file_service)


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["file_path"])
async def fs_create_file(
        file_path: str,
        content: str = "",
        charset: str = "utf-8"
) -> dict:
    """Create text file with initial content."""
    file_service.create_file(file_path, content, charset)
    return {"success": True}


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["file_path"])
async def fs_delete_file(
        file_path: str
) -> dict:
    """Delete single regular file, reject directory."""
    file_service.delete_file(file_path)
    return {"success": True}


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["file_path"])
async def fs_get_file_info(
        file_path: str
) -> dict:
    """Get full file/directory metadata."""
    info: file_service.FileInfo = file_service.get_file_info(file_path)
    return info._asdict()


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["file_path"])
async def fs_is_file_exists(
        file_path: str
) -> dict:
    """Check filesystem entry existence."""
    exists = file_service.is_file_exists(file_path)
    return {"exists": exists}


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["source_file_path", "dest_file_path"])
async def fs_copy_file(
        source_file_path: str,
        dest_file_path: str,
        overwrite: bool
) -> dict:
    """Copy file with metadata, overwrite toggle."""
    file_service.copy_file(source_file_path, dest_file_path, overwrite)
    return {"success": True}


@mcp.tool()
@response_helper
@restrict_workspace(path_argument_names=["source_file_path", "dest_file_path"])
async def fs_move_file(
        source_file_path: str,
        dest_file_path: str,
        overwrite: bool
) -> dict:
    """Move file, control overwrite behavior."""
    file_service.move_file(source_file_path, dest_file_path, overwrite)
    return {"success": True}
