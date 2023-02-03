from dataclasses import dataclass
from src.email.interface.email_interface import IEmail
from src.email.dto.email_dto import EmailDTO
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import os


@dataclass
class SendInBlue(IEmail):
    async def send(self, email: EmailDTO) -> None:
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = os.environ["SEND_IN_BLUE_API_KEY"]
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email_adr} for email_adr in email.recipients if email_adr],
            template_id=email.template_id,
            params=email.params,
        )

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
