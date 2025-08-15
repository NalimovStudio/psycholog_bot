from dishka import Provider, provide, Scope

from source.application.user import CreateUser


class InteractorsProvider(Provider):
    scope = Scope.REQUEST

    create_user = provide(CreateUser)