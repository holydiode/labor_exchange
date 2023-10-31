import factory

from fixtures.users import UserFactory
from models import Job
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)
    user_id = factory.LazyAttribute(lambda x: x.user.id)
    title = factory.Faker("job")
    description = factory.Faker("paragraph")
    salary_from = factory.Faker('pyint', min_value=0, max_value=1_000_000_000)
    salary_to = factory.LazyAttribute(lambda x: x.salary_from + 1_000_000_000)
    is_active = factory.Faker("pybool")
    created_at = factory.Faker("date_time")
