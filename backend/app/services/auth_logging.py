import logging
from datetime import datetime
from sqlalchemy import text

def log_auth_attempt_sp(
    db,
    provider,
    success,
    error_message,
    user_id=None,
    ip_address=None,
):
    try:
        success_bit = 1 if success else 0
        db.execute(
            text("""
                EXEC s_LogAuthAttempt
                    @UserID=:user_id,
                    @Provider=:provider,
                    @Success=:success,
                    @ErrorMessage=:error_message,
                    @IPAddress=:ip_address,
                    @AttemptTime=:attempt_time
            """),
            {
                "user_id": user_id,
                "provider": provider,
                "success": success_bit,
                "error_message": error_message,
                "ip_address": ip_address,
                "attempt_time": datetime.utcnow(),  # Pass current UTC time
            }
        )
        db.commit()
    except Exception as e:
        import logging
        logging.error(f"Failed to log auth attempt: {e}") 