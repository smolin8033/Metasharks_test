from random import choice

import factory
from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from fields.models import Field
from groups.models import StudyGroup
from subjects.models import Subject
from users.models import User

faker = Faker()


class FieldFactory(DjangoModelFactory):
    """Фабрика модели Направления подготовки"""
    name = faker.word()

    class Meta:
        model = Field
        django_get_or_create = (
            "name",
        )


class SubjectFactory(DjangoModelFactory):
    """Фабрика модели Учебной дисциплины"""
    name = faker.word()
    field = SubFactory(FieldFactory)

    class Meta:
        model = Subject
        django_get_or_create = (
            "name",
            "field",
        )


class StudyGroupFactory(DjangoModelFactory):
    """Фабрика модели Учебной группы"""
    number = faker.numerify(text='##')
    field = SubFactory(FieldFactory)

    class Meta:
        model = StudyGroup
        django_get_or_create = (
            "number",
            "field",
        )

    @factory.post_generation
    def subjects(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of subjects were passed in, use them
            for subject in extracted:
                self.subjects.add(subject)


class UserFactory(DjangoModelFactory):
    """Фабрика модели Пользователя"""
    username = faker.word()
    password = faker.password()
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = f'{faker.first_name()}{faker.domain_name()}'
    gender = choice(["M", "F"])
    role = choice(["D", "M", "S"])
    study_group = SubFactory(StudyGroupFactory)

    class Meta:
        model = User
        django_get_or_create = (
            "username",
        )



# from tests.faked_data.factories import UserFactory as U
