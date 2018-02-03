import json

from Core.views.base import TemplateView
from Core.models.auth import Department


class IndexView(TemplateView):
    template_name = 'Core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_id'] = '1345'
        context['employee_name'] = '王蕾'
        context['email'] = '806935949@qq.com'
        with open('Core/views/tmp_menu.txt', 'r') as f:
            context['menu'] = f.read().strip()
        context['deptMap'] = json.dumps(Department.get_departments_dict())
        return context
