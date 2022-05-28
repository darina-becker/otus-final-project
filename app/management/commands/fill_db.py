from django.core.management.base import BaseCommand

from app.models import App, AppKind, AppAgeLimit, AppCategory


class Command(BaseCommand):

    def handle(self, *args, **options):
        kinds = ['applications', 'games']
        for kind in kinds:
            AppKind.objects.get_or_create(name=kind)

        games_category = [
            'action', 'adventure', 'arcade', 'board', 'card', 'casino',
            'educational', 'music', 'puzzle', 'racing', 'role playing',
            'simulation', 'sports', 'strategy', 'trivia', 'word', 'casual'
        ]

        kind_games = AppKind.objects.get(name='games')
        for gc in games_category:
            AppCategory.objects.get_or_create(name=gc, kind=kind_games)

        app_category = [
            'art & design', 'auto & vehicles', 'beauty', 'book & reference', 'business',
            'comics', 'communication', 'dating', 'education', 'entertainment', 'food & drink',
            'health & fitness', 'house & home', 'libraries & demo', 'lifestyle', 'maps & navigation',
            'medical', 'music & audio', 'news and magazines', 'parenting', 'personalization',
            'photography', 'productivity', 'shopping', 'social', 'sports', 'tools',
            'travel & location', 'video players and editors', 'weather'
        ]

        kind_apps = AppKind.objects.get(name='applications')
        for ac in app_category:
            AppCategory.objects.get_or_create(name=ac, kind=kind_apps)

        age_limit = [
            {'name': 'G', 'desc': 'General audiences', 'min_age': 3},
            {'name': 'PG', 'desc': 'Parental guidance suggested', 'min_age': 6},
            {'name': 'PG-13', 'desc': 'Parents strongly cautioned', 'min_age': 13},
            {'name': 'R', 'desc': 'Restricted', 'min_age': 16},
            {'name': 'NC-17', 'desc': 'No One 17 & Under Admitted', 'min_age': 18},
        ]

        for age in age_limit:
            AppAgeLimit.objects.get_or_create(name=age['name'], desc=age['desc'], min_age=age['min_age'])
