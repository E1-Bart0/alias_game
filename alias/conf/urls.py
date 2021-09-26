from conf.views import schema_view
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("player.urls")),
    path("api/", include("game_room.urls")),
    path("api/", include("word.urls")),
    path("", include("frontend.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
