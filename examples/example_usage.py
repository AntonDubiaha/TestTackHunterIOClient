"""Example of using the client for hunter.io and the service."""

import logging
from typing import Any, Dict, List, Optional

from HunterIOClient.main import EmailVerificationService, VerifyClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    api_key: str = 'Your api-key'
    email_to_verify: str = 'Your email'

    hunter_client: VerifyClient = VerifyClient(api_key)
    verification_service: EmailVerificationService = EmailVerificationService()

    # Checking and verifying e-mail
    verification_result: Optional[Dict[str, Any]] = (
        verification_service.create_verification_results(email_to_verify, hunter_client)
    )

    if verification_result:
        logger.info('Verification result for {0}: {1}'.format(email_to_verify, verification_result))
    else:
        logger.error('Email verification failed.')

    # Get of verification results
    all_verification_results: List[Dict[str, Any]] = verification_service.get_results()
    logger.info('All Verification Results: {0}'.format(all_verification_results))

    # Update a test result
    new_verification_result = {'status': 'verified', 'score': 10}
    verification_service.update_verification_result(email_to_verify, new_verification_result)
    updated_verification_results: List[Dict[str, Any]] = verification_service.get_results()
    logger.info('Updated Verification Results: {0}'.format(updated_verification_results))

    # Deleting a test result
    verification_service.delete_verification_result(email_to_verify)

    # Update a test result
    updated_verification_results: List[Dict[str, Any]] = verification_service.get_results()
    logger.info('Updated Verification Results after deleting: {0}'.format(updated_verification_results))
