from user_model import UserRepository
from hypothesis import given, strategies as st

@given(
    name=st.text(min_size=1, max_size=50),
    email=st.emails(),
    age=st.integers(min_value=0, max_value=120)
)
def test_create_and_read_user(name, email, age):
    repo = UserRepository()
    user = repo.create(name, email, age)
    read = repo.read(user.id)
    assert read is not None
    assert read.name == name
    assert read.email == email
    assert read.age == age
    assert read.active is True
