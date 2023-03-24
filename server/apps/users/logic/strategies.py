from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple, Type, TypeAlias

EmailDomain: TypeAlias = str
EmailName: TypeAlias = str
Email: TypeAlias = str
SeparatedEmail: TypeAlias = Tuple[EmailName, EmailDomain]


class Register:
    """Class for registering mail normalization strategies."""

    def __init__(self):
        """Initializes an empty dictionary."""
        self.strategy_by_domain: Dict[
            EmailDomain, 'StrategyEmailNormalize',
        ] = {}
        self.default = None

    def apply(self, strategy: Type['StrategyEmailNormalize']):
        """Method for adding a strategy to a dictionary."""
        for domain in strategy.domains:
            self.strategy_by_domain.setdefault(
                domain, strategy(),
            )

    def get(self, domain: EmailDomain) -> Optional['StrategyEmailNormalize']:
        """Get strategy by domain."""
        if domain not in self.strategy_by_domain.keys():
            return self.default
        return self.strategy_by_domain[domain]

    def apply_default(self, strategy):
        """Setter for default strategy."""
        self.default = strategy()


register = Register()  # type: ignore[no-untyped-call]


class StrategyEmailNormalize(ABC):
    """Abstract class for normalization."""

    domains: Tuple[str, ...]

    @abstractmethod
    def __call__(
        self,
        email_name: EmailName,
        domain_part: EmailDomain,
    ) -> SeparatedEmail:
        """Method to invoke normalization logic."""
        pass  # noqa: WPS420


@register.apply_default
class DefaultStrategy(StrategyEmailNormalize):
    """Default strategy email normalization."""

    def __call__(
        self,
        name: EmailName,
        domain: EmailDomain,
    ) -> SeparatedEmail:
        """Does nothing, just returns name and domain."""
        return name, domain


@register.apply
class YandexStrategyEmailNormalize(StrategyEmailNormalize):
    """Strategy email normalization for yandex mail."""

    domains = ('yandex.ru', 'ya.ru')
    canonical_domain = 'yandex.ru'

    def __call__(
        self,
        name: EmailName,
        domain: EmailDomain,
    ) -> SeparatedEmail:
        """Replaces dots with dashes and cast to canonical domain."""
        name = name.replace('.', '-')
        if domain != self.canonical_domain:
            domain = self.canonical_domain

        return name, domain


@register.apply
class GoogleStrategyEmailNormalize(StrategyEmailNormalize):
    """Strategy email normalization for google mail."""

    domains = ('gmail.com',)

    def __call__(
        self,
        name: EmailName,
        domain: EmailDomain,
    ) -> SeparatedEmail:
        """Removes dots from the name."""
        name = name.replace('.', '')

        return name, domain
