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

class ListingsClient:
    @staticmethod
    async def get_listing(listing_id: int):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{settings.listings_service_url}/v1/listings/{listing_id}")
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Listing not found"
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Failed to fetch listing"
                    )
            except httpx.RequestError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Listings service unavailable"
                )