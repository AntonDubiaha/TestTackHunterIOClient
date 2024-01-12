"""Test task client for hunter.io and service."""

import logging
from typing import Any, Dict, List, Optional

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VerifyClient:
    """Client for verify email."""

    def __init__(self, api_key: str) -> None:
        """
        Initialize the VerifyClient.

        Parameters:
            api_key (str): The API key for authentication.
        """
        self.api_key: str = api_key
        self.base_url: str = 'https://api.hunter.io/v2/'

    def verify_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Verify the given email using the Hunter.io API.

        Parameters:
            email (str): The email address to be verified.

        Returns:
            Optional[Dict[str, Any]]: Verification result as a dictionary if successful, None otherwise.
        """
        endpoint: str = '{0}email-verifier'.format(self.base_url)
        params: Dict[str, str] = {'email': email, 'api_key': self.api_key}  # noqa: WPS110

        try:
            response: requests.Response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            logger.error('Error during email verification: {0}'.format(exc))
            return None


class EmailVerificationService:
    """Service for managing email verification results."""

    def __init__(self) -> None:
        """Initialize the EmailVerificationService."""
        self.verification_results: List[Dict[str, Any]] = []

    def create_verification_results(self, email: str, hunter_client: VerifyClient) -> Optional[Dict[str, Any]]:
        """
        Create a new email verification result.

        Parameters:
            email (str): The email address to be verified.
            hunter_client (VerifyClient): An instance of the VerifyClient.

        Returns:
            Optional[Dict[str, Any]]: Verification result as a dictionary if successful, None otherwise.
        """
        verification_result: Optional[Dict[str, Any]] = hunter_client.verify_email(email)
        self.verification_results.append(verification_result)
        return verification_result

    def get_results(self) -> List[Dict[str, Any]]:
        """
        Get all email verification results.

        Returns:
            List[Dict[str, Any]]: A list of email verification results.
        """
        return self.verification_results

    def update_verification_result(self, email: str, new_result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update verification result data for existing email..

        Parameters:
            email (str): The email address associated with the result to be updated.
            new_result (Dict[str, Any]): The new verification result data.

        Returns:
            Optional[Dict[str, Any]]: Updated verification result as a dictionary if successful, None otherwise.
        """
        for verification_result in self.verification_results:
            if verification_result['data']['email'] == email:
                verification_result['data'].update(new_result)
                return verification_result
        return None

    def delete_verification_result(self, email: str) -> None:
        """
        Delete verification results associated with the current email.

        Parameters:
            email (str): The email address associated with the result to be deleted.
        """
        self.verification_results = [result for result in self.verification_results if result['data']['email'] != email]
