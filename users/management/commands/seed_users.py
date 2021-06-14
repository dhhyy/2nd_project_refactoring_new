import bcrypt
from faker.proxy import Faker
import jwt
from os import name
from django.core.management.base import BaseCommand
from django_seed import Seed
from django_seed.seeder import Seeder
from users.models import User
from products.models import City

class Command(BaseCommand):
    help = '랜덤 유저 생성'

    def add_arguments(self, parser):
        parser.add_argument(
                "--total",
                default=2,
                type=int,
                help='몇 명의 유저 데이터를 만드드냐'
                )

    def handle(self, *args, **options):
        total = options.get("total")

        password = '12341234'

        seeder = Seed.seeder()
        seeder.add_entity(
                User, 
                total,
                {
                    "email" : lambda x: seeder.faker.email(),
                    "password" : bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                    "name" : lambda x: seeder.faker.name()
                    }
                )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{total} users created!"))

# foreignkey 연결 카테고리를 ㅁall로 가지고 온다 / 랜덤 함수 안에 넣는다 / 생각을 쉽게 쉽게

class Command(BaseCommand):
    help = '도시 생성'

    def add_arguments(self, parser):
        parser.add_argument(
                "--total",
                default=2,
                type=int,
                help = '도시를 몇 개를 생성할 것인가'
                )

    def handle(self, *args, **options):
        total = options.get("total")
        seeder = Seed.seeder()
        fake = Faker(["ko_KR"])

        seeder.add_entity(
                City,
                total,
                {
                    'name' : fake.city()
                    }
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{total} cities created!"))
