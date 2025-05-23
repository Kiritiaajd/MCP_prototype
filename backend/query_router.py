# backend/query_router.py

from handlers.tat_handler import handle_tat_query
from handlers.loan_handler import handle_loan_query
from handlers.enterprise_handler import handle_enterprise_query
from handlers.exposure_handler import handle_exposure_query
from handlers.cam_handler import handle_cam_query
from handlers.timeline_handler import handle_timeline_query
from handlers.personnel_handler import handle_personnel_query

def route_query(query: str) -> dict:
    """
    Routes the incoming query to the appropriate handler based on keywords.
    """
    query_lower = query.lower()

    # TAT or turnaround time related
    if any(keyword in query_lower for keyword in ["tat", "turnaround", "review time", "cam tat", "credit tat", "final tat"]):
        return handle_tat_query(query)

    # Loan application status, approvals
    elif any(keyword in query_lower for keyword in ["loan", "application", "approved", "rejected", "sanctioned"]):
        return handle_loan_query(query)

    # Enterprise or company profile
    elif any(keyword in query_lower for keyword in ["enterprise", "company", "firm", "org", "organization"]):
        return handle_enterprise_query(query)

    # Credit exposure, risk details
    elif any(keyword in query_lower for keyword in ["exposure", "credit exposure", "risk", "current exposure", "proposed exposure"]):
        return handle_exposure_query(query)

    # CAM creation or appraisal processes
    elif any(keyword in query_lower for keyword in ["cam", "credit appraisal", "appraisal note"]):
        return handle_cam_query(query)

    # Timelines, delays, approval flow
    elif any(keyword in query_lower for keyword in ["approval", "timeline", "delay", "iteration", "approval date"]):
        return handle_timeline_query(query)

    # RM, Analyst, RBH, RCH, JD performance
    elif any(keyword in query_lower for keyword in ["rm", "relationship manager", "analyst", "rbh", "rch", "jd", "committee"]):
        return handle_personnel_query(query)

    # Default fallback
    else:
        return {
            "status": "error",
            "message": "Query not matched to any known context. Please use keywords like 'loan', 'enterprise', 'tat', etc."
        }
