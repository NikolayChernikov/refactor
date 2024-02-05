"""Requests routes module."""
from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from pydantic import PositiveInt

from app.internal.services import Requests, Services
from app.pkg import models
from app.pkg.models import Tag

router = APIRouter(prefix="/requests", tags=["Requests to IT"])


@router.get(
    "/",
    response_model=List[models.ReadRequest],
    status_code=status.HTTP_200_OK,
    description="Read all requests",
)
@inject
async def read_all(
    service: Requests = Depends(Provide[Services.requests]),
) -> List[models.Request]:
    """Read all data.

    Args:
        service: service requests.

    Returns: list with requests.
    """
    return await service.read_all()


@router.get(
    "/by_time",
    response_model=List[models.RequestFull],
    status_code=status.HTTP_200_OK,
    description="Read all requests",
)
@inject
async def read_all_by_time(
    time_from: int,
    time_to: int,
    service: Requests = Depends(Provide[Services.requests]),
) -> List[models.RequestFull]:
    """Read all data by time.

    Args:
        time_from: time from.
        time_to: time to.
        service: requests service.

    Returns: list with requests.
    """
    return await service.read_all_by_time(time_from, time_to)


@router.get(
    "/{id:int}/",
    response_model=models.ReadRequest,
    status_code=status.HTTP_200_OK,
    description="Read request",
)
@inject
async def read(
    id: PositiveInt,  # pylint: disable=redefined-builtin
    service: Requests = Depends(Provide[Services.requests]),
) -> models.Request:
    """Read data.

    Args:
        id: request id.
        service: requests service.

    Returns: request.
    """
    return await service.read(id=id)


@router.post(
    "/",
    response_model=models.ReadRequest,
    status_code=status.HTTP_200_OK,
    description="Create request",
)
@inject
async def create(
    cmd: models.CreateRequestCommand,
    service: Requests = Depends(Provide[Services.requests]),
) -> models.Request:
    """Insert data.

    Args:
        cmd: create request command.
        service: requests service.

    Returns: request.
    """
    return await service.create(cmd=cmd)


@router.patch(
    "/",
    response_model=models.ReadRequest,
    status_code=status.HTTP_200_OK,
    description="Update request",
)
@inject
async def update(
    cmd: models.UpdateRequestCommand,
    service: Requests = Depends(Provide[Services.requests]),
) -> models.Request:
    """Update data.

    Args:
        cmd: update request command.
        service: requests service.

    Returns: request.
    """
    return await service.update(cmd=cmd)


@router.delete(
    "/{id:int}/",
    response_model=models.ReadRequest,
    status_code=status.HTTP_200_OK,
    description="Delete request",
)
@inject
async def delete(
    id: PositiveInt,  # pylint: disable=redefined-builtin
    service: Requests = Depends(Provide[Services.requests]),
) -> models.Request:
    """Delete data.

    Args:
        id: request id.
        service: requests service.

    Returns: request.
    """
    return await service.delete(id=id)


@router.post(
    "/{id:int}/comment",
    response_model=models.Comment,
    status_code=status.HTTP_200_OK,
    description="Add comment to post",
)
@inject
async def add_comment(
    id: PositiveInt,  # pylint: disable=redefined-builtin
    cmd: models.Comment,
    service: Requests = Depends(Provide[Services.requests]),
) -> models.Comment:
    """Read data.

    Args:
        id: request id.
        cmd: comment model.
        service: requests service.

    Returns: comment model.
    """
    return await service.add_comment(id, cmd)


@router.get(
    "/tags",
    response_model=List[Tag],
    status_code=status.HTTP_200_OK,
    description="Get all tags",
)
@inject
async def get_all_tags(
    service: Requests = Depends(Provide[Services.requests]),
) -> List[Tag]:
    """Read data.

    Args:
        service: requests service.

    Returns: list with tag.
    """
    return await service.get_all_tags()
