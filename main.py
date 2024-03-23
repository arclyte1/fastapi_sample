from typing import List

from fastapi import FastAPI, Response, Request

import persistance as ps
from dto import GroupDetailsDto, GroupDto, CreateParticipant, CreateGroup, ParticipantDto, ParticipantDetailsDto

app = FastAPI()


def run_with_404(f):
    res = None
    try:
        res = f()
    finally:
        if res:
            return res
        else:
            return Response(status_code=404)


@app.post("/group")
async def create_group(data: CreateGroup):
    return ps.create_group(data).id


@app.get("/groups", response_model=List[GroupDto])
async def get_groups():
    return ps.get_groups()


@app.get("/group/{id}", response_model=GroupDetailsDto | None)
async def get_group_details(id: int):
    def f():
        return ps.get_group_details(id)

    return run_with_404(f)


@app.post("/group/{id}/participant")
async def create_participant(id: int, data: CreateParticipant):
    def f():
        return ps.create_participant(data, id).id

    return run_with_404(f)


@app.post("/group/{id}/toss", response_model=List[ParticipantDetailsDto])
async def toss(id: int):
    def f():
        if res := ps.group_toss(id):
            return res
        else:
            return Response(status_code=409)

    return run_with_404(f)


@app.put("/group/{id}", response_model=GroupDetailsDto)
async def update_group(request: Request, id: int):
    body = await request.json()

    def f():
        return ps.update_group(id, body)

    return run_with_404(f)


@app.delete("/group/{id}")
async def delete_group(id: int):
    def f():
        return ps.delete_group(id)

    return run_with_404(f)


@app.delete("/group/{g_id}/participant/{p_id}")
async def delete_participant(g_id: int, p_id: int):
    def f():
        return ps.delete_participant(g_id, p_id)

    return run_with_404(f)


@app.get("/group/{g_id}/participant/{p_id}/recipient", response_model=ParticipantDto | None)
async def get_recipient(g_id: int, p_id: int):
    def f():
        return ps.get_recipient(g_id, p_id)

    return run_with_404(f)
