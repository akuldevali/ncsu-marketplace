import httpx
from fastapi import HTTPException, status
from config import settings

class AuthClient:
    @staticmethod
    async def validate_token(token: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{settings.auth_service_url}/v1/auth/validate",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid token"
                    )
            except httpx.RequestError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Authentication service unavailable"
                )