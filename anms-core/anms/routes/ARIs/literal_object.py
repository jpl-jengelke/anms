#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 The Johns Hopkins University Applied Physics
# Laboratory LLC.
#
# This file is part of the Asynchronous Network Managment System (ANMS).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This work was performed for the Jet Propulsion Laboratory, California
# Institute of Technology, sponsored by the United States Government under
# the prime contract 80NM0018D0004 between the Caltech and NASA under
# subcontract 1658085.
#
from typing import List

from fastapi import APIRouter, Depends
from fastapi import status
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.engine import Result

from anms.components.schemas import ARIs
from anms.models.relational import get_async_session
from anms.models.relational.literal_object import LiteralObject
from anms.shared.opensearch_logger import OpenSearchLogger

logger = OpenSearchLogger(__name__, log_console=True)

router = APIRouter(tags=["ARIs"])


@router.get("", status_code=status.HTTP_200_OK, response_model=Page[ARIs.LiteralObject])
async def paged_Literal_object(params: Params = Depends()):
    async with get_async_session() as session:
        return await paginate(session, select(LiteralObject), params)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[ARIs.LiteralObject])
async def all_literal_object():
    stmt = select(LiteralObject)
    async with get_async_session() as session:
        result: Result = await session.scalars(stmt)
        return result.all()


@router.get("/id/{obj_actual_definition_id}", status_code=status.HTTP_200_OK, response_model=ARIs.LiteralObject)
async def literal_object_by_id(obj_actual_definition_id: int):
    stmt = select(LiteralObject).where(LiteralObject.obj_actual_definition_id == obj_actual_definition_id)
    async with get_async_session() as session:
        result: Result = await session.scalars(stmt)
        return result.one_or_none()
