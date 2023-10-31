import factory

from fixtures.jobs import JobFactory
from fixtures.users import UserFactory
from models import Response
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class ResponseFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Response

    id = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)
    user_id = factory.LazyAttribute(lambda x: x.user.id)
    job = factory.SubFactory(JobFactory)
    job_id = factory.LazyAttribute(lambda x: x.job.id)
    message = factory.Faker("paragraph")
