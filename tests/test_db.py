from application.models import User


def test_user_model(db):
    user = User(
        username="my username",
        email = "email@easdf.dk"
    )
    db.session.add(user)
    db.session.commit()

    getuser = User.query.filter_by(username=user.username).first()

    assert getuser.username is user.username
