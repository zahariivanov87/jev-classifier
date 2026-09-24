import os
from dotenv import load_dotenv
from typesafe_sdk import TypeSafeClient, Choice, Score, Noul

# Load environment variables from .env file
load_dotenv()


def main():
    # Initialize the official TypeSafe client
    # Automatically reads TYPESAFE_API_KEY from environment
    with TypeSafeClient() as client:
        print("=== TypeSafe AI (Jev Model) Demo ===")

        # 1. Define the input state
        user_ticket = {
            "user_id": "usr_9981",
            "message": "Hello, my card was charged twice for the same monthly subscription! I would like a refund.",
            "account_tier": "VIP"
        }

        print(f"\nInput State:\n{user_ticket}\n")

        # 2. Call the System One model (Jev)
        response = client.system_one(
            state=user_ticket,
            questions={
                "category": Choice(
                    instructions="What is this ticket about?",
                    criteria={
                        "billing": "Payment issues, duplicate charges, or invoices",
                        "technical": "Bugs, outages, or technical issues",
                        "other": "Does not fit any category"
                    }
                ),
                "urgency": Score(
                    instructions="Assess customer service urgency",
                    levels=["Low", "Medium", "High", "Critical"]
                ),
                "requires_refund": Noul(
                    statement="The user explicitly requests a monetary refund."
                )
            }
        )

        # 3. Access typed results
        print("--- Jev Output ---")

        # Category (Choice)
        cat_res = response.choices["category"]
        print(f"Category: {cat_res.choice}")
        print(f"Confidence: {cat_res.confidence:.2%}")

        # Urgency (Score)
        urg_res = response.scores["urgency"]
        print(f"Urgency: {urg_res.score}")

        # Refund (Noul)
        ref_res = response.nouls["requires_refund"]
        print(f"Requests Refund: {'YES' if ref_res.probability > 0.5 else 'NO'} ({ref_res.probability:.2%})")


if __name__ == "__main__":
    main()