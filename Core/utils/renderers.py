from rest_framework import renderers


class BrowsableAPIWithoutFormRenderer(renderers.BrowsableAPIRenderer):
    def get_rendered_html_form(self, data, view, method, request):
        if method in ('PUT', 'POST', 'DELETE'):
            return None
        return super().get_rendered_html_form(data, view, method, request)

    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context['display_edit_forms'] = False
        return context
