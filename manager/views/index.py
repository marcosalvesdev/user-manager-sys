from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # For now I'll let it this way till the index page is builded
        return HttpResponseRedirect(reverse_lazy("manager"))
