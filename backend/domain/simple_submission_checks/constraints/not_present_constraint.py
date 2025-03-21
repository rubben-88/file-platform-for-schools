import os
from pathlib import Path

from pydantic import BaseModel

from domain.simple_submission_checks.constraints.constraint_result import (
    ConstraintType,
    NotPresentConstraintResult,
)


class NotPresentConstraint(BaseModel):
    type: ConstraintType = ConstraintType.NOT_PRESENT
    file_or_directory_name: str

    def validate_constraint(self, path: Path) -> NotPresentConstraintResult:
        directory = os.listdir(path)

        if self.file_or_directory_name in directory:
            return NotPresentConstraintResult(file_or_directory_name=self.file_or_directory_name, is_ok=False)

        return NotPresentConstraintResult(file_or_directory_name=self.file_or_directory_name, is_ok=True)
