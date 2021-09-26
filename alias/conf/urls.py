from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("player.urls")),
    path("api/", include("game_room.urls")),
    path("api/", include("word.urls")),
    path("", include("frontend.urls")),
    path("docs", include_docs_urls(title="Alias-API")),
    path(
        "schema",
        get_schema_view(
            title="Alias-Game", description="API for all things", version="1.0.0"
        ),
        name="openapi-schema",
    ),
]
