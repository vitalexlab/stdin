from sqlalchemy import Engine
from sqlalchemy.orm import Session

#
# def insert(db_engine: Engine) -> None:
#     with Session(db_engine) as session:
#         # spongebob = User(
#         #     name="spongebob",
#         #     fullname="Spongebob Squarepants",
#         #     addresses=[Address(email_address="spongebob@sqlalchemy.org")],
#         # )
#         # sandy = User(
#         #     name="sandy",
#         #     fullname="Sandy Cheeks",
#         #     addresses=[
#         #         Address(email_address="sandy@sqlalchemy.org"),
#         #         Address(email_address="sandy@squirrelpower.org"),
#         #      ],
#         # )
#         # patrick = User(name="patrick", fullname="Patrick Star")
#         # session.add_all([spongebob, sandy, patrick])
#         #
#         # session.commit()