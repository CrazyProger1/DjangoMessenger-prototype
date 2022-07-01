from django.core.management.base import BaseCommand, CommandError
from users.models import User
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Creates superuser (short command)'

    def add_arguments(self, parser):
        parser.add_argument('-p', nargs='?', type=str, help='Specify admin password', dest='password', default='admin')
        parser.add_argument('-u', nargs='?', type=str, help='Specify admin username', dest='username', default='admin')
        parser.add_argument('-e', nargs='?', type=str, help='Specify admin email', dest='email',
                            default='admin@admin.com')

    def handle(self, *args, **options):
        password = options.get('password')
        username = options.get('username')
        email = options.get('email')

        try:
            pass
            User.objects.create_superuser(username, email, password)
        except IntegrityError:
            print(f"User with username '{username}' already exists")
            return

        print(f"Admin succesefully created(name='{username}' email='{email}' password='{password}')")
