from django.db import migrations

def create_listing_categories(apps, schema_editor):
    ListingCategory = apps.get_model('marketplace', 'ListingCategory')

    categories = [
        ('furniture', 'Furniture'),
        ('electronics', 'Electronics'),
        ('clothes', 'Clothes'),
        ('makeup', 'Makeup'),
        ('books', 'Books'),
        ('toys', 'Toys'),
        ('tools', 'Tools'),
        ('vehicles', 'Vehicles'),
        ('real_estate', 'Real Estate'),
        ('other', 'Other'),
    ]

    for code, name in categories:
        ListingCategory.objects.update_or_create(code=code, defaults={'name': name})

class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0011_listingcategory_customuser_biography_and_more'),  # replace with last migration
    ]

    operations = [
        migrations.RunPython(create_listing_categories),
    ]
