"""
Push notification service using Expo Push API.

Expo Push API docs: https://docs.expo.dev/push-notifications/sending-notifications/
"""
import httpx
import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.notification import get_user_tokens, deactivate_token

logger = logging.getLogger(__name__)

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"


@dataclass
class PushMessage:
    to: str
    title: str
    body: str
    data: Optional[Dict[str, Any]] = None
    sound: str = "default"
    channel_id: str = "default"
    priority: str = "high"


async def send_push_notification(messages: List[PushMessage]) -> Dict[str, Any]:
    """
    Send push notifications via Expo Push API.
    
    Args:
        messages: List of PushMessage objects to send
        
    Returns:
        Response from Expo Push API
    """
    if not messages:
        return {"status": "no_messages"}
    
    payload = [
        {
            "to": msg.to,
            "title": msg.title,
            "body": msg.body,
            "data": msg.data or {},
            "sound": msg.sound,
            "channelId": msg.channel_id,
            "priority": msg.priority,
        }
        for msg in messages
    ]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                EXPO_PUSH_URL,
                json=payload,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Expo Push API error: {e.response.status_code} - {e.response.text}")
        return {"error": str(e)}
    except Exception as e:
        logger.error(f"Failed to send push notification: {e}")
        return {"error": str(e)}


async def send_push_to_user(
    db: AsyncSession,
    user_id: str,
    title: str,
    body: str,
    data: Optional[Dict[str, Any]] = None,
    channel_id: str = "default"
) -> bool:
    """
    Send a push notification to all devices of a specific user.
    
    Args:
        db: Database session
        user_id: ID of the user to notify
        title: Notification title
        body: Notification body text
        data: Optional data payload
        channel_id: Android notification channel
        
    Returns:
        True if at least one notification was sent successfully
    """
    tokens = await get_user_tokens(db, user_id)
    
    if not tokens:
        logger.info(f"No push tokens found for user {user_id}")
        return False
    
    messages = [
        PushMessage(
            to=token.token,
            title=title,
            body=body,
            data=data,
            channel_id=channel_id
        )
        for token in tokens
    ]
    
    result = await send_push_notification(messages)
    
    # Handle failed tokens
    if "data" in result:
        for i, ticket in enumerate(result["data"]):
            if ticket.get("status") == "error":
                error_type = ticket.get("details", {}).get("error")
                if error_type in ("DeviceNotRegistered", "InvalidCredentials"):
                    # Token is invalid, deactivate it
                    await deactivate_token(db, tokens[i].token)
                    logger.info(f"Deactivated invalid token: {tokens[i].token[:20]}...")
    
    return "error" not in result


async def send_session_invite_notification(
    db: AsyncSession,
    invitee_id: str,
    inviter_name: str,
    session_title: str,
    session_id: str
) -> bool:
    """Send a push notification for a session invite."""
    return await send_push_to_user(
        db=db,
        user_id=invitee_id,
        title="Session Invite 🏋️",
        body=f"{inviter_name} invited you to: {session_title}",
        data={
            "type": "session_invite",
            "session_id": session_id
        },
        channel_id="sessions"
    )


async def send_friend_request_notification(
    db: AsyncSession,
    addressee_id: str,
    requester_name: str,
    friendship_id: str
) -> bool:
    """Send a push notification for a friend request."""
    return await send_push_to_user(
        db=db,
        user_id=addressee_id,
        title="New Friend Request 👋",
        body=f"{requester_name} wants to be your gym buddy!",
        data={
            "type": "friend_request",
            "friendship_id": friendship_id
        },
        channel_id="social"
    )
