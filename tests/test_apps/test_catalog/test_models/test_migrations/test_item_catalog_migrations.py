import pytest
from django_test_migrations.migrator import Migrator

from server.apps.catalog.urls import app_name


def test_initial0001(migrator: Migrator) -> None:
    """Tests the initial migration forward application."""
    old_state = migrator.apply_initial_migration((app_name, None))
    with pytest.raises(LookupError):
        old_state.apps.get_model(app_name, 'CatalogItem')

    new_state = migrator.apply_tested_migration((app_name, '0001_initial'))
    model = new_state.apps.get_model(app_name, 'CatalogItem')

    assert model.objects.create(
        name='Pomidor',
    )
