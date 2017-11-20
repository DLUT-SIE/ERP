from Core.views import TemplateView, LoginRequiredMixin
from Messaging.models import Message, DocumentFile


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        news = Message.news.all().order_by('-create_date')
        announcements = Message.announcements.all().order_by('-create_date')
        documents = DocumentFile.public_files.all().order_by(
            '-message__create_date')
        context['news'] = news
        context['announcements'] = announcements
        context['documents'] = documents

        # Expose consts
        context['MESSAGE_CATEGORY_NEWS'] = 0
        context['MESSAGE_CATEGORY_ANNOUNCEMENT'] = 1
        context['MESSAGE_CATEGORY_PERSONAL'] = 2
        return context
