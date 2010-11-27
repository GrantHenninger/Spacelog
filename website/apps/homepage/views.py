from django.views.generic import TemplateView
from backend.util import timestamp_to_seconds
from backend.api import LogLine, Act

class HomepageView(TemplateView):
    template_name = 'homepage/homepage.html'

    def get_context_data(self):
        acts = [
            (x+1, act)
            for x, act in
            enumerate(Act.Query(self.request.redis_conn, self.request.mission.name))
        ]
        quote_timestamp = self.request.redis_conn.srandmember(
            "mission:%s:homepage_quotes" % self.request.mission.name,
        )
        quote = LogLine(
            self.request.redis_conn,
            self.request.mission.main_transcript,
            int(timestamp_to_seconds(quote_timestamp)),
        )
        return {
            "acts": acts,
            "quote": quote,
        }

