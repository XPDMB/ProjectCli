"""
URL configuration — API ที่ /api/v1/ และหน้าเว็บที่รากโดเมน
"""

from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

from pathlib import Path

from .settings import FRONTEND_ROOT

_frontend_pages = Path(FRONTEND_ROOT) / "pages"
_DOC_ROOT = str(_frontend_pages)


def _serve_page(name: str):
    def view(request):
        return serve(request, name, document_root=_DOC_ROOT)

    return view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("clinic_api.urls")),
    path("", _serve_page("index.html")),
    path("index.html", _serve_page("index.html")),
    path("login.html", _serve_page("login.html")),
    path("register.html", _serve_page("register.html")),
    path("admin-board.html", _serve_page("admin-board.html")),
    path("owner-board.html", _serve_page("owner-board.html")),
    path("booking.html", _serve_page("booking.html")),
    path("vet-board.html", _serve_page("vet-board.html")),
    path("assistant-board.html", _serve_page("assistant-board.html")),
    path("assets/<path:path>", serve, {"document_root": str(FRONTEND_ROOT / "assets")}),
    path("js/<path:path>", serve, {"document_root": str(FRONTEND_ROOT / "js")}),
]
