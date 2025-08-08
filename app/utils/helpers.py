import json
from typing import Dict, Optional


# Redis keys helpers
def user_session_key(phone: str) -> str:
    return f"session:{phone}"


def ephemeral_trip_key(phone: str, trip_id: str) -> str:
    return f"trip_temp:{phone}:{trip_id}"


# Example of session hash fields
def create_user_session_data(
    current_intent: Optional[str] = None,
    last_interaction_time: Optional[int] = None,
    cached_itinerary: Optional[Dict] = None,
    temporary_data: Optional[Dict] = None,
) -> Dict[str, str]:
    session = {}
    if current_intent:
        session["currentIntent"] = current_intent
    if last_interaction_time:
        session["lastInteractionTime"] = str(last_interaction_time)
    if cached_itinerary:
        session["cachedItinerary"] = json.dumps(cached_itinerary)
    if temporary_data:
        session["temporaryData"] = json.dumps(temporary_data)
    return session


# Example ephemeral trip data
def create_ephemeral_trip_data(
    draft_activities: Optional[Dict] = None,
    collaborators_pending: Optional[Dict] = None,
    ai_response_cache: Optional[str] = None,
) -> Dict[str, str]:
    data = {}
    if draft_activities:
        data["draftActivities"] = json.dumps(draft_activities)
    if collaborators_pending:
        data["collaboratorsPending"] = json.dumps(collaborators_pending)
    if ai_response_cache:
        data["aiResponseCache"] = ai_response_cache
    return data
