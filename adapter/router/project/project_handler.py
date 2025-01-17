import io
from fastapi import UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from domain.project.project_service import ProjectService

from domain.project.project_service import ProjectServiceError, ProjectServiceErrorExtra
from domain.project.project_entity import Project
from pydantic import BaseModel
import base64

class FindProjectByIdResponse(BaseModel):
    message: str
    project: Project | None

class FindProjectPosterByIdResponse(BaseModel):
    message: str
    project: Project | None

class CreateProjectResponse(BaseModel):
    message: str
    project: Project | None

class UpdateProjectResponse(BaseModel):
    message: str
    project: Project | None

class UpdateProjectPosterResponse(BaseModel):
    message: str
    poster_base64: str | None

class FindProjectByUserIdResponse(BaseModel):
    message: str
    projects: list[Project] | None

class ProjectHandler:
    
    def __init__(self, project_service: ProjectService):
        self.project_service = project_service

    def find_project_by_id(self, project_id: str) -> JSONResponse:
        res = self.project_service.find_project_by_id(project_id)
        if isinstance(res, ProjectServiceErrorExtra):
            content = jsonable_encoder(CreateProjectResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                project=None
            ))
            return JSONResponse(content=content, status_code=500, media_type="application/json")
        
        elif isinstance(res, ProjectServiceError):
            update_project_response = jsonable_encoder(FindProjectByIdResponse(
                message=f"{res.name}: {res.message}",
                project=None
            ))
            return JSONResponse(content=update_project_response, status_code=400, media_type="application/json")
        else:
            project = res
            find_project_by_id_response = jsonable_encoder(FindProjectByIdResponse(
                message="project found",
                project=project
            ))
            return JSONResponse(content=find_project_by_id_response, status_code=200, media_type="application/json")

    def create_project(self, project: Project) -> JSONResponse:
        res = self.project_service.create_project(project)
        if isinstance(res, ProjectServiceErrorExtra):
            content = jsonable_encoder(CreateProjectResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                project=None
            ))
            return JSONResponse(content=content, status_code=500, media_type="application/json")
        
        elif isinstance(res, ProjectServiceError):
            update_project_response = jsonable_encoder(FindProjectByIdResponse(
                message=f"{res.name}: {res.message}",
                project=None
            ))
            return JSONResponse(content=update_project_response, status_code=400, media_type="application/json")
        else:
            project = res
            create_project_response = jsonable_encoder(CreateProjectResponse(
                message="project was successully created",
                project=project
            ))
            return JSONResponse(content=create_project_response, status_code=200, media_type="application/json")

    def update_project(self, project: Project) -> JSONResponse:
        res = self.project_service.update_project(project)
        if isinstance(res, ProjectServiceErrorExtra):
            content = jsonable_encoder(CreateProjectResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                project=None
            ))
            return JSONResponse(content=content, status_code=500, media_type="application/json")
        
        elif isinstance(res, ProjectServiceError):
            update_project_response = jsonable_encoder(FindProjectByIdResponse(
                message=f"{res.name}: {res.message}",
                project=None
            ))
            return JSONResponse(content=update_project_response, status_code=400, media_type="application/json")
        else:
            project = res
            update_project_response = jsonable_encoder(UpdateProjectResponse(
                message="project was successfully updated",
                project=project
            ))
            return JSONResponse(content=update_project_response, status_code=200, media_type="application/json")
    
    def update_project_poster(self, project_id: str, poster: UploadFile) -> JSONResponse:
        posterbase64 = str(base64.b64encode(poster.file.read()))[2:-1]
        res = self.project_service.update_project_poster(project_id, posterbase64)

        if isinstance(res, ProjectServiceErrorExtra):
            content = jsonable_encoder(CreateProjectResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                project=None
            ))
            return JSONResponse(content=content, status_code=500, media_type="application/json")
        
        elif isinstance(res, ProjectServiceError):
            update_project_response = jsonable_encoder(FindProjectByIdResponse(
                message=f"{res.name}: {res.message}",
                project=None
            ))
            return JSONResponse(content=update_project_response, status_code=400, media_type="application/json")
        else:
            update_project_response = jsonable_encoder(UpdateProjectPosterResponse(
                message="poster was successfully updated",
                poster_base64=res
            ))
            return JSONResponse(content=update_project_response, status_code=200, media_type="application/json")

    def find_project_poster_by_id(self, project_id: str) -> StreamingResponse | JSONResponse:
        res = self.project_service.find_project_poster_by_id(project_id)
        if isinstance(res, ProjectServiceErrorExtra):
            content = jsonable_encoder(CreateProjectResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                project=None
            ))
            return JSONResponse(content=content, status_code=500, media_type="application/json")
        
        elif isinstance(res, ProjectServiceError):
            update_project_response = jsonable_encoder(FindProjectByIdResponse(
                message=f"{res.name}: {res.message}",
                project=None
            ))
            return JSONResponse(content=update_project_response, status_code=400, media_type="application/json")
        else:
            return StreamingResponse(content=io.BytesIO(res), status_code=200, media_type="image/jpg")
    
    def find_project_by_user_id(self, user_id: str) -> JSONResponse:
        
        res = self.project_service.find_project_by_user_id(user_id)
        if isinstance(res, ProjectServiceErrorExtra):
            content = jsonable_encoder(CreateProjectResponse(
                message=f"{res.name}: {res.message}. {res.extra_message}",
                project=None
            ))
            return JSONResponse(content=content, status_code=500, media_type="application/json")
        
        elif isinstance(res, ProjectServiceError):
            update_project_response = jsonable_encoder(FindProjectByIdResponse(
                message=f"{res.name}: {res.message}",
                project=None
            ))
            return JSONResponse(content=update_project_response, status_code=400, media_type="application/json")
        else:
            content = jsonable_encoder(FindProjectByUserIdResponse(
                message="below are projects found",
                projects=res
            ))
            return JSONResponse(content=content, status_code=200, media_type="application/json")