from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'ex03/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors_title'] = ['black', 'red', 'blue', 'green']

        increase = range(0, 250, 5)
        max = [245] * 50
        black = zip(increase, increase, increase)
        red = zip(max, increase, increase)
        blue = zip(increase, increase, max)
        green = zip(increase, max, increase)
        colors_rows = zip(black, red, blue, green)
        context['colors_rows'] = colors_rows
        return context
