import os
import textwrap

root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(root)

entities = [
    ('admin', 'Admin', '/admins', 'Admins'),
    ('booking', 'Booking', '/bookings', 'Bookings'),
    ('branch', 'Branch', '/branches', 'Branches'),
    ('branch_schedule', 'BranchSchedule', '/branch-schedules', 'BranchSchedules'),
    ('broadcast_general', 'BroadcastGeneral', '/broadcasts/general', 'BroadcastGeneral'),
    ('broadcast_personal', 'BroadcastPersonal', '/broadcasts/personal', 'BroadcastPersonal'),
    ('chat', 'Chat', '/chats', 'Chats'),
    ('client', 'Client', '/clients', 'Clients'),
    ('coordinator', 'Coordinator', '/coordinators', 'Coordinators'),
    ('doctor', 'Doctor', '/doctors', 'Doctors'),
    ('message', 'Message', '/messages', 'Messages'),
    ('result', 'Result', '/results', 'Results'),
    ('staff', 'Staff', '/staff', 'Staff'),
    ('test', 'Test', '/tests', 'Tests'),
    ('user', 'User', '/users', 'Users'),
]


def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(textwrap.dedent(content).lstrip())

message_src = os.path.join(root, 'app', 'schemas', 'messsage.py')
message_dst = os.path.join(root, 'app', 'schemas', 'message.py')
if os.path.exists(message_src) and not os.path.exists(message_dst):
    os.replace(message_src, message_dst)

write_file(os.path.join(root, 'app', 'routes', 'dependencies.py'), '''
from typing import Generator
from sqlmodel import Session
from database.db import engine


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
''')

for module_name, model_name, prefix, tag in entities:
    create_schema = f"{model_name}Create"
    response_schema = f"{model_name}Response"
    repo_prefix = module_name

    repo_content = f'''
from typing import Any, Dict
from sqlmodel import Session
from models import {model_name}
from repositories.repository import create_item, delete_item, get_all_items, get_item_by_id, update_item


def get_all_{repo_prefix}(session: Session):
    return get_all_items(session, {model_name})


def get_{repo_prefix}_by_id(session: Session, item_id: Any):
    return get_item_by_id(session, {model_name}, item_id)


def create_{repo_prefix}(session: Session, data: Dict[str, Any]):
    return create_item(session, {model_name}, data)


def update_{repo_prefix}(session: Session, item_id: Any, data: Dict[str, Any]):
    return update_item(session, {model_name}, item_id, data)


def delete_{repo_prefix}(session: Session, item_id: Any):
    return delete_item(session, {model_name}, item_id)
'''
    write_file(os.path.join(root, 'app', 'repositories', f'{module_name}.py'), repo_content)

    service_content = f'''
from typing import Any
from sqlmodel import Session
from repositories.{module_name} import (
    create_{repo_prefix},
    delete_{repo_prefix},
    get_{repo_prefix}_by_id,
    get_all_{repo_prefix},
    update_{repo_prefix},
)


def list_{repo_prefix}(session: Session):
    return get_all_{repo_prefix}(session)


def get_{repo_prefix}(session: Session, item_id: Any):
    return get_{repo_prefix}_by_id(session, item_id)


def create_{repo_prefix}_item(session: Session, payload: Any):
    data = payload.dict(exclude_none=True)
    return create_{repo_prefix}(session, data)


def update_{repo_prefix}_item(session: Session, item_id: Any, payload: Any):
    data = payload.dict(exclude_none=True)
    return update_{repo_prefix}(session, item_id, data)


def delete_{repo_prefix}_item(session: Session, item_id: Any):
    return delete_{repo_prefix}(session, item_id)
'''
    write_file(os.path.join(root, 'app', 'services', f'{module_name}.py'), service_content)

    route_content = f'''
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from routes.dependencies import get_session
from schemas.{module_name} import {create_schema}, {response_schema}
from services.{module_name} import (
    create_{repo_prefix}_item,
    delete_{repo_prefix}_item,
    get_{repo_prefix},
    list_{repo_prefix},
    update_{repo_prefix}_item,
)

router = APIRouter(prefix="{prefix}", tags=["{tag}"])


@router.post("/", response_model={response_schema}, status_code=status.HTTP_201_CREATED)
def create_{repo_prefix}(payload: {create_schema}, session: Session = Depends(get_session)):
    return create_{repo_prefix}_item(session, payload)


@router.get("/", response_model=List[{response_schema}])
def read_{repo_prefix}s(session: Session = Depends(get_session)):
    return list_{repo_prefix}(session)


@router.get("/{{item_id}}", response_model={response_schema})
def read_{repo_prefix}(item_id: str, session: Session = Depends(get_session)):
    item = get_{repo_prefix}(session, item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.put("/{{item_id}}", response_model={response_schema})
def update_{repo_prefix}(item_id: str, payload: {create_schema}, session: Session = Depends(get_session)):
    item = update_{repo_prefix}_item(session, item_id, payload)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.delete("/{{item_id}}", status_code=status.HTTP_204_NO_CONTENT)
def delete_{repo_prefix}(item_id: str, session: Session = Depends(get_session)):
    deleted = delete_{repo_prefix}_item(session, item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return None
'''
    write_file(os.path.join(root, 'app', 'routes', f'{module_name}.py'), route_content)

main_imports = ['from fastapi import APIRouter\n']
for module_name, _, _, _ in entities:
    main_imports.append(f'from .{module_name} import router as {module_name}_router\n')
main_imports.append('\nrouter = APIRouter()\n\n')
for module_name, _, _, _ in entities:
    main_imports.append(f'router.include_router({module_name}_router)\n')
write_file(os.path.join(root, 'app', 'routes', 'main.py'), ''.join(main_imports))

write_file(os.path.join(root, 'app', 'main.py'), '''
from fastapi import FastAPI
from routes.main import router as api_router

app = FastAPI()
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
''')

print('Generated entity-specific route, service, and repository modules.')
