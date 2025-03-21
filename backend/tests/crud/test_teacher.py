# test_teacher.py
import unittest

from sqlmodel import SQLModel

from domain.logic.teacher import create_teacher, get_all_teachers, get_teacher
from tests.crud.test_main import get_db, test_engine


class TestTeacher(unittest.TestCase):
    def setUp(self) -> None:
        SQLModel.metadata.drop_all(test_engine)
        SQLModel.metadata.create_all(test_engine)
        self.session = next(get_db())

    def tearDown(self) -> None:
        self.session.rollback()
        self.session.close()

    def test_create_and_get_teacher(self) -> None:
        teacher = create_teacher(self.session, "Test Teacher", "testteacher@gmail.com")
        retrieved_teacher = get_teacher(self.session, teacher.id)
        self.assertEqual(teacher.id, retrieved_teacher.id)

    def test_get_all_teachers(self) -> None:
        create_teacher(self.session, "Test Teacher 1", "testteacher1@gmail.com")
        create_teacher(self.session, "Test Teacher 2", "testteacher2@gmail.com")
        self.assertEqual(len(get_all_teachers(self.session)), 2)


if __name__ == "__main__":
    unittest.main()
