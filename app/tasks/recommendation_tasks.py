"""
Recommendation background job placeholders.
"""


def precompute_recommendations_for_user(user_id: str) -> None:
    raise NotImplementedError(
        "Recommendation precomputation needs a dedicated worker and event table implementation."
    )


def precompute_all_user_recommendations(batch_size: int = 100) -> None:
    raise NotImplementedError(
        "Recommendation precomputation needs a dedicated worker and event table implementation."
    )
