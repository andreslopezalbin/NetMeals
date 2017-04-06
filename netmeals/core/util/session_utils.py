from core.util.session_constants import *


def set_context_with_session_key(session, key, context, msg):
    if session.get(key):
        context[key] = session.get(key)
        del session[key]
        context['success_msg'] = msg


def set_context_with_activity_session(session, context):
    set_context_with_session_key(session, SESSION_SUBSCRIPTION_SUCCEEDED, context, 'Successfully subscribed!')
    set_context_with_session_key(session, SESSION_UNSUBSCRIPTION_SUCCEEDED, context, 'Successfully unsubscribed!')
    set_context_with_session_key(session, SESSION_ACTIVITY_CREATED_SUCCEEDED, context, 'Activity created successfully!')
    set_context_with_session_key(session, SESSION_ACTIVITY_MOD_SUCCEEDED, context, 'Activity modified successfully!')
    set_context_with_session_key(session, SESSION_ACTIVITY_DEL_SUCCEEDED, context, 'Activity deleted successfully!')