class MockEmailSender:
    async def send_registration_email(self, email:str):
        print(f"Email sent to {email}")
