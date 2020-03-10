from monarch.forms.admin.oauth2 import OauthAppSchema, OauthAppDetailSchema
from monarch.models.oauth2 import OAuthApp
from monarch.utils.api import parse_pagination, Bizs
from monarch.utils.common import gen_random_key


def get_oauth_app_list(data):
    name = data.get("name")
    data = parse_pagination(
        OAuthApp.query_oauth_app(name)
    )
    result, pagination = data["result"], data["pagination"]
    oauth_app_list = OauthAppSchema().dump(result, many=True).data
    ret_data = {"list": oauth_app_list, "pagination": pagination}
    return Bizs.success(data=ret_data)


def create_oauth_app(data):
    OAuthApp.create(
        client_id=gen_random_key(),
        client_secret=gen_random_key(),
        status=OAuthApp.APPROVED,
        name=data.get("name"),
        description=data.get("description"),
        homepage=data.get("homepage"),
        redirect_url=data.get("redirect_url"),
        white_list=data.get("white_list"),
    )
    return Bizs.success()


def get_oauth_app(oauth_app_id):
    oauth_app = OAuthApp.get(oauth_app_id)
    if not oauth_app:
        return Bizs.not_found()

    oauth_app_data = OauthAppDetailSchema().dump(oauth_app).data
    return Bizs.success(oauth_app_data)


def update_oauth_app(oauth_app_id, data):
    oauth_app = OAuthApp.get(oauth_app_id)
    if not oauth_app:
        return Bizs.not_found()

    oauth_app.update(
        description=data.get("description"),
        homepage=data.get("homepage"),
        redirect_url=data.get("redirect_url"),
        white_list=data.get("white_list"),
        name=data.get("name")
    )
    return Bizs.success()


def delete_oauth_app(oauth_app_id):
    oauth_app = OAuthApp.get(oauth_app_id)
    if not oauth_app:
        return Bizs.not_found()

    oauth_app.delete()
    return Bizs.success()
