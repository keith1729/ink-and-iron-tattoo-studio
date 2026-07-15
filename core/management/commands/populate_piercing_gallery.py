import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import PiercingImage

VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif')

class Command(BaseCommand):
    help = 'Creates gallery entries for any photos sitting in media/piercings/ that are not yet in the gallery'

    def handle(self, *args, **options):
        folder = os.path.join(settings.MEDIA_ROOT, 'piercings')
        os.makedirs(folder, exist_ok=True)
        existing = set(PiercingImage.objects.values_list('image', flat=True))
        created_count = 0

        for filename in os.listdir(folder):
            if not filename.lower().endswith(VALID_EXTENSIONS):
                continue
            relative_path = f'piercings/{filename}'
            if relative_path in existing:
                continue
            title = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
            PiercingImage.objects.create(title=title, image=relative_path)
            created_count += 1
            self.stdout.write(f'Added: {title}')

        self.stdout.write(self.style.SUCCESS(f'Done. Created {created_count} new gallery entries.'))