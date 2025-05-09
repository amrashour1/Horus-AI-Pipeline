session_id = create_session("ملخص الجلسة")
if session_id:
    add_message(session_id, "user", "رسالة المستخدم")
    add_message(session_id, "system", "رد النظام")