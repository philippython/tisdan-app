from fastapi import APIRouter
from .admin import router as admin_router
from .booking import router as booking_router
from .branch import router as branch_router
from .branch_schedule import router as branch_schedule_router
from .broadcast_general import router as broadcast_general_router
from .broadcast_personal import router as broadcast_personal_router
from .chat import router as chat_router
from .client import router as client_router
from .coordinator import router as coordinator_router
from .doctor import router as doctor_router
from .message import router as message_router
from .result import router as result_router
from .staff import router as staff_router
from .test import router as test_router
from .user import router as user_router

router = APIRouter()

router.include_router(admin_router)
router.include_router(booking_router)
router.include_router(branch_router)
router.include_router(branch_schedule_router)
router.include_router(broadcast_general_router)
router.include_router(broadcast_personal_router)
router.include_router(chat_router)
router.include_router(client_router)
router.include_router(coordinator_router)
router.include_router(doctor_router)
router.include_router(message_router)
router.include_router(result_router)
router.include_router(staff_router)
router.include_router(test_router)
router.include_router(user_router)
