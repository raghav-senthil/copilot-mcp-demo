from dataclasses import dataclass
from datetime import date
from typing import Dict


@dataclass
class Policy:
    policy_id: str
    customer_name: str
    coverage_type: str
    premium: float
    active: bool = True


@dataclass
class Claim:
    claim_id: str
    policy_id: str
    description: str
    amount: float
    status: str = "pending"


class InsuranceApplication:
    """In-memory insurance policy and claims application."""

    def __init__(self) -> None:
        self.policies: Dict[str, Policy] = {}
        self.claims: Dict[str, Claim] = {}

    def create_policy(
        self,
        policy_id: str,
        customer_name: str,
        coverage_type: str,
        premium: float,
    ) -> Policy:
        if policy_id in self.policies:
            raise ValueError(f"Policy {policy_id} already exists")
        if premium <= 0:
            raise ValueError("Premium must be greater than zero")

        policy = Policy(policy_id, customer_name, coverage_type, premium)
        self.policies[policy_id] = policy
        return policy

    def create_claim(
        self,
        claim_id: str,
        policy_id: str,
        description: str,
        amount: float,
    ) -> Claim:
        if claim_id in self.claims:
            raise ValueError(f"Claim {claim_id} already exists")
        policy = self.policies.get(policy_id)
        if policy is None:
            raise ValueError(f"Policy {policy_id} was not found")
        if not policy.active:
            raise ValueError(f"Policy {policy_id} is inactive")
        if amount <= 0:
            raise ValueError("Claim amount must be greater than zero")

        claim = Claim(claim_id, policy_id, description, amount)
        self.claims[claim_id] = claim
        return claim

    def approve_claim(self, claim_id: str) -> Claim:
        claim = self.claims.get(claim_id)
        if claim is None:
            raise ValueError(f"Claim {claim_id} was not found")
        if claim.status != "pending":
            raise ValueError(f"Claim {claim_id} is already {claim.status}")

        claim.status = "approved"
        return claim


def main() -> None:
    app = InsuranceApplication()

    policy = app.create_policy(
        policy_id="POL-1001",
        customer_name="Avery Johnson",
        coverage_type="home",
        premium=125.50,
    )
    claim = app.create_claim(
        claim_id="CLM-5001",
        policy_id=policy.policy_id,
        description="Water damage repair",
        amount=2400.00,
    )
    approved_claim = app.approve_claim(claim.claim_id)

    print(f"Policy created: {policy}")
    print(f"Claim created on {date.today()}: {claim}")
    print(f"Claim approved: {approved_claim}")


if __name__ == "__main__":
    main()
