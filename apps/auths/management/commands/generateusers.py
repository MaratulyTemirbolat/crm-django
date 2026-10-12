from datetime import datetime
from typing import Any
from random import choice

from django.core.management.base import BaseCommand

from apps.auths.models import CustomUser


class Command(BaseCommand):

    MAILBOX_DOMAINS = (
        "example.com",
        "kbtu.kz",
    )
    DEFAULT_PASSWORD = "12345"

    def __get_email_from_full_name(self, full_name: str) -> str:
        """Get email from full name.Temirbolat MAratuly -> temirbolat.maratuly""" 
        return full_name.lower().replace(" ", ".") + choice(self.MAILBOX_DOMAINS)



    def __create_users(self, number_of_users: int) -> None:
        """Create users."""

        created_users_cnt: int = 0

        users_to_create: list[CustomUser] = []

        i: int
        for i in range(number_of_users):

            full_name: str = f"User {choice(range(1, 1000))}"
            email: str = self.__get_email_from_full_name(full_name)
            user_with_email_exists: bool = CustomUser.objects.filter(email=email).exists()

            if not user_with_email_exists:
                users_to_create.append(
                    CustomUser(
                        email=email,
                        full_name=full_name,
                        password=self.DEFAULT_PASSWORD,
                    )
                )


            # SELECT * FROM auths_customuser WHERE email=email LIMIT 1;
            # user_with_email: CustomUser | None = CustomUser.objects.filter(email=email).first()


            # if not user_with_email:
            #     CustomUser.objects.create( # INSERT INTO auths_customuser (email, ...) VALUES (email, ...);
            #         email=email,
            #         full_name=full_name,
            #         password=self.DEFAULT_PASSWORD,
            #     )
            #     created_users_cnt += 1

            # _, created =CustomUser.objects.get_or_create(
            #     email=email,
            #     defaults={
            #         "full_name": full_name,
            #         "password": self.DEFAULT_PASSWORD,
            #     }
            # )
            # created_users_cnt = created_users_cnt + 1 if created else created_users_cnt
            # print("Created user with email: {} and full name: {}".format(email, full_name))

        CustomUser.objects.bulk_create(users_to_create)
        print(f"Created {len(users_to_create)} users out of {number_of_users} requested.")
        # print(f"Created {created_users_cnt} users out of {number_of_users} requested.")


    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """Command entry point."""

        start_time: datetime = datetime.now()

        self.__create_users(number_of_users=100000)

        print(
            "The whole process to generate data took: {} seconds".format(
                (datetime.now() - start_time).total_seconds()
            )
        )