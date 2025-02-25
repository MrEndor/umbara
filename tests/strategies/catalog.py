from base64 import b64decode
from random import choice, randrange
from typing import List

from django.core.files.uploadedfile import SimpleUploadedFile
from hypothesis import strategies
from hypothesis.extra import django

from server.apps.catalog.constants import CATALOG_ITEM_KEYWORDS
from server.apps.catalog.models import (
    CatalogCategory,
    CatalogItem,
    CatalogTag,
    ImageItem,
)

EMPTY_PIXEL = b64decode((
    'iVBORw0KGgoAAAANSUhEU' +
    'gAAAAEAAAABCAAAAAA6fp' +
    'tVAAAACklEQVQYV2P4DwA' +
    'BAQEAWk1v8QAAAABJRU5Er' +
    'kJggg=='
))


@strategies.composite
def item_text_strategies(draw):
    """Keyword Text Generation Strategy."""
    text: List[str] = draw(strategies.text(min_size=10)).split()
    word = choice(CATALOG_ITEM_KEYWORDS)  # noqa: S311

    text.insert(
        randrange(0, len(text)),  # noqa: S311
        word,
    )

    return ''.join(text)


def include_tags(
    product: CatalogItem, tags: List[CatalogTag],
) -> CatalogItem:
    """Function to add tags."""
    product.tags.add(*tags)

    return product


def include_images(
    product: CatalogItem,
    image_content: bytes,
):
    """Function to add images."""
    image = SimpleUploadedFile(
        'cat.jpg',
        content=image_content,
        content_type='image/jpeg',
    )
    image.product = product  # type: ignore[attr-defined]

    product.image = image

    image_item = ImageItem.objects.create(
        image=image,
        product=product,
    )
    image_item.save()
    product.gallery.add(image_item)
    product.save()

    return product


def generate_product_with_dependencies(
    products: strategies.SearchStrategy[CatalogItem],
) -> strategies.SearchStrategy[CatalogItem]:
    """Strategy for Generating a Tagged Product."""
    product_with_tags = strategies.builds(
        include_tags,
        products,
        base_tags_strategy,
    )

    return strategies.builds(
        include_images,
        product_with_tags,
    )


base_tags_strategy = strategies.lists(
    django.from_model(
        CatalogTag,
        id=strategies.integers(
            min_value=1,
            max_value=(2 ** 63) - 1,
        ),
        name=strategies.text(
            alphabet=strategies.from_regex(
                '^[а-яА-Яa-zA-Z]$', fullmatch=True,
            ),
            min_size=10,
            max_size=150,
        ),
    ),
    min_size=1,
    unique=True,
)

base_images_strategy = django.from_model(
    ImageItem,
    product=strategies.none(),
)

base_category_strategy = django.from_model(
    CatalogCategory,
    id=strategies.integers(
        min_value=1,
        max_value=(2 ** 63) - 1,
    ),
    name=strategies.text(
        alphabet=strategies.from_regex(
            '^[а-яА-Яa-zA-Z]$', fullmatch=True,
        ),
        min_size=100,
        max_size=150,
    ),
    slug=strategies.text(
        alphabet=strategies.from_regex(
            '^[0-9-_a-zA-Z]$', fullmatch=True,
        ),
        min_size=100,
        max_size=200,
    ),
)

base_item_strategy = generate_product_with_dependencies(
    django.from_model(
        CatalogItem,
        category=base_category_strategy,
        text=item_text_strategies(),
        image=strategies.none(),
    ),
)
