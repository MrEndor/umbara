import pytest
from django_test_migrations.migrator import Migrator

from server.apps.catalog.urls import app_name

CatalogCategory = 'CatalogCategory'


def test_initial0001(migrator: Migrator) -> None:
    """Tests the initial migration forward application."""
    old_state = migrator.apply_initial_migration((app_name, None))
    with pytest.raises(LookupError):
        old_state.apps.get_model(app_name, CatalogCategory)

    new_state = migrator.apply_tested_migration((app_name, '0001_initial'))
    model = new_state.apps.get_model(app_name, 'CatalogCategory')

    assert model.objects.create(
        name='qwerty',
        weight=20000,
        slug='asd290as',
    )


def test_normalize0002(migrator: Migrator) -> None:
    """Tests the 0002_normalize migration forward application."""
    old_state = migrator.apply_initial_migration((app_name, '0001_initial'))
    old_state.apps.get_model(app_name, CatalogCategory)

    new_state = migrator.apply_tested_migration((app_name, '0002_normalize'))
    model = new_state.apps.get_model(app_name, CatalogCategory)

    assert model.objects.create(
        name='qwerty',
        weight=20000,
        slug='asd290as',
    )
