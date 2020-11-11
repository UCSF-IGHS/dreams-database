import factory
from faker import Factory
from DreamsApp.models import (
    Client,
    InterventionType,
    InterventionCategory,
    ExternalOrganisationType,
    ExternalOrganisation,
    HTSResult,
    PregnancyTestResult,
    ImplementingPartner,
)


class ExternalOrganisationTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExternalOrganisationType


class InterventionCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InterventionCategory


class InterventionTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InterventionType

    code = 1001


class HTSResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HTSResult

    code = 1001


class ExternalOrganisationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExternalOrganisation

    code = 1001


class PregnancyTestResultFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PregnancyTestResult

    code = 501


class ImplementingPartnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ImplementingPartner

    code = 601
