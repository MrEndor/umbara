from server.apps.users.logic.strategies import (
    Email,
    EmailDomain,
    EmailName,
    register,
)


def clean_tags(raw_name: EmailName):
    """Removes tags in the mail title."""
    if '+' not in raw_name:
        return raw_name
    name, tags = raw_name.split('+', 1)
    return name


def assembly(name: EmailName, domain: EmailDomain) -> Email:
    """Collects mail from name and domain."""
    return '{name}@{domain}'.format(
        name=name, domain=domain,
    )


def normalize_email(email: Email) -> Email:
    """Mail normalization function."""
    if email == '':
        return email

    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        return email

    domain_part = domain_part.lower()
    email_name = clean_tags(email_name)

    strategy = register.get(domain_part)

    if not strategy:
        return assembly(email_name, domain_part)
    return assembly(*strategy(email_name, domain_part))
